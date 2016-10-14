# -*- coding: utf-8 -*-
"""Filters for WAStD Observations."""
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _

import django_filters
from django_filters import filters, widgets
# from leaflet.forms.widgets import LeafletWidget

from wastd.observations.models import Area, Encounter, AnimalEncounter


class LocationListFilter(SimpleListFilter):
    """A custom ListFilter to filter Encounters by location."""

    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Marine Protected Area')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'where'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [(a.pk, a.name) for a in
                Area.objects.filter(area_type=Area.AREATYPE_MPA)]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            a = Area.objects.get(pk=self.value())
            return queryset.filter(where__within=a.geom)
        return queryset

class EncounterFilter(django_filters.FilterSet):
    """Encounter Filter.

    https://django-filter.readthedocs.io/en/latest/usage.html
    """
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=_("Name supports partial match, e.g. searching for "
                    "WA12 will return encounters with WA123 and WA124."))
    source_id = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=_("Source ID supports partial match.")
        )
    when = filters.DateFromToRangeFilter(
        help_text="Date format: YYYY-mm-dd, e.g. 2015-12-31",
        widget=widgets.RangeWidget(attrs={'placeholder': 'YYYY-mm-dd'}))
    # where = django_filters.CharFilter(
    #     widget=LeafletWidget(attrs={
    #         'map_height': '400px',
    #         'map_width': '100%',
    #         'display_raw': 'False',
    #         'map_srid': 4326,
    #         }))

    class Meta:
        """Options for EncounterFilter."""

        model = Encounter


class AnimalEncounterFilter(EncounterFilter):
    """AnimalEncounter Filter."""

    class Meta:
        """Options for AnimalEncounterFilter."""
        model = AnimalEncounter
