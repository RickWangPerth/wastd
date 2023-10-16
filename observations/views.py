from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, TemplateView, ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django_fsm_log.models import StateLog
from wastd.utils import ListViewBreadcrumbMixin, DetailViewBreadcrumbMixin, ResourceDownloadMixin
from django.http import JsonResponse
from django.db import connection

from .admin import (
    EncounterAdmin,
    AnimalEncounterAdmin,
    TurtleNestEncounterAdmin,
    LineTransectEncounterAdmin,
)
from .filters import (
    SurveyFilter,
    EncounterFilter,
    AnimalEncounterFilter,
    TurtleNestEncounterFilter,
    LineTransectEncounterFilter,
)
from .models import (
    Survey,
    Encounter,
    AnimalEncounter,
    TurtleNestEncounter,
    LineTransectEncounter,
    TagObservation,
)
from .resources import (
    SurveyResource,
    EncounterResource,
    AnimalEncounterResource,
    TurtleNestEncounterResource,
    LineTransectEncounterResource,
)


class MapView(TemplateView):
    template_name = "observations/map.html"


class SurveyList(ListViewBreadcrumbMixin, ResourceDownloadMixin, ListView):
    model = Survey
    template_name = "default_list.html"
    paginate_by = 20
    filter_class = SurveyFilter
    resource_class = SurveyResource
    resource_formats = ["csv", "xlsx"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_filter"] = SurveyFilter(self.request.GET, queryset=self.get_queryset())
        context["object_count"] = self.get_queryset().count()
        context["page_title"] = f"{settings.SITE_CODE} | Surveys"
        return context

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related("reporter", "site", "encounter_set").order_by("-start_time")
        return SurveyFilter(self.request.GET, queryset=qs).qs


class SurveyDetail(DetailViewBreadcrumbMixin, DetailView):
    model = Survey

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context["page_title"] = f"{settings.SITE_CODE} | Survey {obj.pk}"
        return context


def close_survey_duplicates(request, pk):
    """Close duplicates for a given Survey PK with the request user as actor.

    All duplicate Surveys will be curated and marked as "not production".
    The given Survey will be curated and marked as "production",
    adopt all Encounters from all duplicate surveys, and adjust its duration.

    See Survey.close_duplicates() for implementation details.
    """
    s = Survey.objects.get(pk=pk)
    msg = s.close_duplicates(actor=request.user)
    messages.success(request, msg)
    return HttpResponseRedirect(s.get_absolute_url())


class EncounterList(ListViewBreadcrumbMixin, ResourceDownloadMixin, ListView):
    model = Encounter
    template_name = "default_list.html"
    paginate_by = 20
    filter_class = EncounterFilter
    resource_class = EncounterResource
    resource_formats = ['csv', 'xlsx']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_filter"] = EncounterFilter(
            self.request.GET, queryset=self.get_queryset()
        )
        context["model_admin"] = EncounterAdmin
        context["page_title"] = f"{settings.SITE_CODE} | Encounters"
        return context

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related("observer", "area", "site").order_by("-when")
        return EncounterFilter(self.request.GET, queryset=qs).qs


class EncounterDetail(DetailViewBreadcrumbMixin, DetailView):
    model = Encounter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context["page_title"] = f"{settings.SITE_CODE} | Encounter {obj.pk}"
        return context


class EncounterCurate(LoginRequiredMixin, SingleObjectMixin, View):
    """Minimal view to handle HTTP request to mark a record as curated.
    """
    model = Encounter

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # FIXME: Permission check
        if not request.user.is_staff:
            return HttpResponseForbidden("You do not have permission to curate this record")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.curate(by=request.user, description="Curated record as trustworthy")
        obj.save()
        messages.success(request, f"Curated {obj} as trustworthy")
        return HttpResponseRedirect(obj.get_absolute_url())


class EncounterFlag(LoginRequiredMixin, SingleObjectMixin, View):
    """Minimal view to handle HTTP request to mark a record as flagged.
    """

    def dispatch(self, request, *args, **kwargs):
        # FIXME: Permission check
        if not request.user.is_staff:
            return HttpResponseForbidden("You do not have permission to flag this record")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.flag(by=request.user, description="Flagged record as untrustworthy")
        obj.save()
        messages.warning(request, f"Flagged {obj} as untrustworthy")
        return HttpResponseRedirect(obj.get_absolute_url())


class EncounterReject(LoginRequiredMixin, SingleObjectMixin, View):
    """Minimal view to handle HTTP request to mark a record as rejected.
    """

    def dispatch(self, request, *args, **kwargs):
        # FIXME: Permission check
        if not request.user.is_staff:
            return HttpResponseForbidden("You do not have permission to reject this record")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.reject(by=request.user, description="Rejected record as untrustworthy")
        obj.save()
        messages.error(request, f"Rejected {obj} as untrustworthy")
        return HttpResponseRedirect(obj.get_absolute_url())


class AnimalEncounterList(ListViewBreadcrumbMixin, ResourceDownloadMixin, ListView):
    model = AnimalEncounter
    template_name = "default_list.html"
    paginate_by = 20
    filter_class = AnimalEncounterFilter
    resource_class = AnimalEncounterResource
    resource_formats = ["csv", "xlsx"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        context["list_filter"] = AnimalEncounterFilter(self.request.GET, queryset=qs)
        context["model_admin"] = AnimalEncounterAdmin
        context["object_count"] = qs.count()
        context["page_title"] = f"{settings.SITE_CODE} | Animal encounters"
        return context

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related("observer", "reporter", "area", "site").order_by("-when")
        return AnimalEncounterFilter(self.request.GET, queryset=qs).qs


class AnimalEncounterDetail(DetailViewBreadcrumbMixin, DetailView):
    model = AnimalEncounter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context["tag_observations"] = TagObservation.objects.filter(encounter__in=[obj])
        context["state_logs"] = StateLog.objects.for_(obj)
        context["page_title"] = f"{settings.SITE_CODE} | Animal encounter {obj.pk}"
        return context


class AnimalEncounterCurate(EncounterCurate):
    model = AnimalEncounter


class AnimalEncounterFlag(EncounterFlag):
    model = AnimalEncounter


class AnimalEncounterReject(EncounterReject):
    model = AnimalEncounter


class TurtleNestEncounterList(ListViewBreadcrumbMixin, ResourceDownloadMixin, ListView):
    model = TurtleNestEncounter
    template_name = "default_list.html"
    paginate_by = 20
    filter_class = TurtleNestEncounterFilter
    resource_class = [
        TurtleNestEncounterResource,
    ]
    resource_formats = ['csv', 'xlsx']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        context["list_filter"] = TurtleNestEncounterFilter(self.request.GET, queryset=qs)
        context["model_admin"] = TurtleNestEncounterAdmin
        context["object_count"] = qs.count()
        context["page_title"] = f"{settings.SITE_CODE} | Turtle nest encounters"
        return context

    def get_queryset(self):
        # FIXME: filtering via permissions model.
        qs = super().get_queryset()
        return TurtleNestEncounterFilter(self.request.GET, queryset=qs).qs


class TurtleNestEncounterDetail(DetailViewBreadcrumbMixin, DetailView):
    # FIXME: filtering via permissions model.
    model = TurtleNestEncounter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context["state_logs"] = StateLog.objects.for_(obj)
        context["page_title"] = f"{settings.SITE_CODE} | Turtle nest encounter {obj.pk}"
        return context


class TurtleNestEncounterCurate(EncounterCurate):
    model = TurtleNestEncounter


class TurtleNestEncounterFlag(EncounterFlag):
    model = TurtleNestEncounter


class TurtleNestEncounterReject(EncounterReject):
    model = TurtleNestEncounter


class LineTransectEncounterList(ListViewBreadcrumbMixin, ResourceDownloadMixin, ListView):
    model = LineTransectEncounter
    template_name = "default_list.html"
    paginate_by = 20
    filter_class = LineTransectEncounterFilter
    resource_class = LineTransectEncounterResource
    resource_formats = ['csv', 'xlsx']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_filter"] = LineTransectEncounterFilter(self.request.GET, queryset=self.get_queryset())
        context["model_admin"] = LineTransectEncounterAdmin
        return context

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related("observer", "reporter", "area", "site").order_by("-when")
        return LineTransectEncounterFilter(self.request.GET, queryset=qs).qs


class LineTransectEncounterDetail(DetailViewBreadcrumbMixin, DetailView):
    model = LineTransectEncounter

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required

#This just dumps the database as json for use by external tools such as PowerBI or Shiny
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@login_required 
def dbdump(request):
    query = '''
SELECT 
    e."id",
    e."source",
    e."source_id",
    ctype_o."model" AS "turtle_observation_model",  -- Add the model name for turtle observation in
    ctype_tag."model" AS "tag_observation_model",   -- Add the model name for tag observation
    ctype_hatch."model" AS "hatch_observation_model", -- Add the model name for hatch observation
    e."status",
    TO_CHAR(e."when" AT TIME ZONE \'Australia/Perth\', \'YYYY-MM-DD\') AS "date",
    TO_CHAR(e."when" AT TIME ZONE \'Australia/Perth\', \'HH24:MI:SS\') AS "time",
    CASE 
        WHEN EXTRACT(HOUR FROM e."when" AT TIME ZONE \'Australia/Perth\') < 12 THEN
            TO_CHAR(e."when" AT TIME ZONE \'Australia/Perth\' - INTERVAL \'1 day\', \'YYYY-MM-DD\')
        ELSE
            TO_CHAR(e."when" AT TIME ZONE \'Australia/Perth\', \'YYYY-MM-DD\')
    END AS "turtle_date",
    site."name" AS "site_name",
    ST_Y(e."where") as latitude,
    ST_X(e."where") as longitude,
    e."survey_id",
    area."name" AS "area_name",
    e."name",
    obs."name" AS "observer",
    rep."name" AS "reporter",
    e."encounter_type",
    e."comments",
    t."encounter_ptr_id",
    t."nest_age",
    t."nest_type",
    t."species",
    t."habitat",
    t."disturbance",
    t."nest_tagged",
    t."logger_found",
    t."eggs_counted",
    t."hatchlings_measured",
    t."fan_angles_measured",
    o."id" as "turtle_observation_id",
    o."source" as "turtle_observation_source",
    o."source_id" as "turtle_observation_source_id",
    n."eggs_laid",
    n."egg_count",
    n."no_egg_shells",
    n."no_live_hatchlings_neck_of_nest",
    n."no_live_hatchlings",
    n."no_dead_hatchlings",
    n."no_undeveloped_eggs",
    n."no_unhatched_eggs",
    n."no_unhatched_term",
    n."no_depredated_eggs",
    n."nest_depth_top",
    n."nest_depth_bottom",
    n."sand_temp",
    n."air_temp",
    n."water_temp",
    n."egg_temp",
    n."comments" AS "turtle_observation_comments",
    tag."comments" AS "tag_observation_comments",
    hatch."bearing_to_water_degrees",
    hatch."bearing_leftmost_track_degrees",
    hatch."bearing_rightmost_track_degrees",
    hatch."no_tracks_main_group_max",
    hatch."outlier_tracks_present",
    hatch."path_to_sea_comments",
    hatch."hatchling_emergence_time_known",
    hatch."hatchling_emergence_time",
    hatch."hatchling_emergence_time_accuracy",
    hatch."cloud_cover_at_emergence_known",
    hatch."cloud_cover_at_emergence",
    tag."observation_ptr_id" as "tag_observation_id",
    tag."status" AS "nest_tag_status",
    tag."flipper_tag_id",
    tag."date_nest_laid",
    tag."tag_label"
FROM 
    "observations_turtlenestencounter" t
INNER JOIN 
    "observations_encounter" e ON (t."encounter_ptr_id" = e."id")
LEFT JOIN 
    "observations_area" area ON (e."area_id" = area."id")
LEFT JOIN 
    "observations_area" site ON (e."site_id" = site."id")
LEFT JOIN 
    "observations_survey" survey ON (e."survey_id" = survey."id")
LEFT JOIN 
    "users_user" obs ON (e."observer_id" = obs."id")
LEFT JOIN 
    "users_user" rep ON (e."reporter_id" = rep."id")
LEFT JOIN 
    "observations_observation" o ON (e."id" = o."encounter_id" AND o."polymorphic_ctype_id" IN (26))
LEFT JOIN 
    "django_content_type" ctype_o ON (o."polymorphic_ctype_id" = ctype_o."id")  -- Join for turtle observation model name
LEFT JOIN 
    "observations_turtlenestobservation" n ON (o."id" = n."observation_ptr_id")
LEFT JOIN 
    "observations_observation" obs_tag ON (e."id" = obs_tag."encounter_id" AND obs_tag."polymorphic_ctype_id" IN (38))
LEFT JOIN 
    "django_content_type" ctype_tag ON (obs_tag."polymorphic_ctype_id" = ctype_tag."id")  -- Join for tag observation model name
LEFT JOIN 
    "observations_nesttagobservation" tag ON (obs_tag."id" = tag."observation_ptr_id")
LEFT JOIN 
    "observations_observation" obs_hatch ON (e."id" = obs_hatch."encounter_id" AND obs_hatch."polymorphic_ctype_id" IN (279))
LEFT JOIN 
    "django_content_type" ctype_hatch ON (obs_hatch."polymorphic_ctype_id" = ctype_hatch."id")  -- Join for hatch observation model name
LEFT JOIN 
    "observations_turtlehatchlingemergenceobservation" hatch ON (obs_hatch."id" = hatch."observation_ptr_id")
WHERE 
    survey."production" = true
ORDER BY 
    e."when" DESC
    '''
    with connection.cursor() as cursor:
        cursor.execute(query)
        # Fetch column names from the cursor description
        columns = [col[0] for col in cursor.description]
        # Convert the result to a list of dictionaries
        results = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    return JsonResponse({'results': results}, safe=False)
