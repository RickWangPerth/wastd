from django.conf import settings
from django.contrib import messages
from django.db import connections, DatabaseError
from django.db.models import Q, Exists, OuterRef
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic.edit import FormMixin
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.http import JsonResponse, QueryDict
from .models import TrtPlaces, TrtSpecies
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
import os
import json
import re

from wastd.utils import Breadcrumb, PaginateMixin
from .models import (
    TrtTurtles,
    TrtTags,
    TrtPitTags,
    TrtEntryBatches,
    TrtDataEntry,
    TrtPersons,
    TrtObservations,
    Template
)
from .forms import TrtDataEntryForm, SearchForm, TrtEntryBatchesForm, TemplateForm


class HomePageView(LoginRequiredMixin, TemplateView):
    """
    A view for the home page.

    Attributes:
        template_name (str): The name of the template to be used for rendering the view.
    """

    template_name = "wamtram2/home.html"


class EntryBatchesListView(LoginRequiredMixin, ListView):
    """
    A view that displays a list of entry batches.

    Attributes:
        model (Model): The model class to use for the list view.
        template_name (str): The name of the template to use for rendering the list view.
        context_object_name (str): The name of the variable to use in the template for the list of objects.
        paginate_by (int): The number of objects to display per page.

    Methods:
        get_queryset(): Returns the queryset of objects for the list view.
        get_context_data(**kwargs): Returns the context data for rendering the list view.
    """

    model = TrtEntryBatches
    template_name = "trtentrybatches_list.html"
    context_object_name = "batches"
    paginate_by = 50

    def dispatch(self, request, *args, **kwargs):
        # FIXME: Permission check
        if not (
            request.user.groups.filter(name="Tagging Data Entry").exists()
            or request.user.groups.filter(name="Tagging Data Curation").exists()
            or request.user.is_superuser
        ):
            return HttpResponseForbidden(
                "You do not have permission to view this record"
            )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """
        Returns the queryset of objects for the list view.

        Returns:
            QuerySet: The queryset of objects.
        """
        queryset = super().get_queryset()

        # Check if the user has requested to filter by TrtEntryBatches that have TrtDataEntrys with no observation_id
        if (
            "filter" in self.request.GET
            and self.request.GET["filter"] == "no_observation_id"
        ):
            # Subquery that checks if a TrtDataEntry with no observation_id exists for a TrtEntryBatch
            has_dataentry_no_observation_id = Exists(
                TrtDataEntry.objects.filter(
                    entry_batch_id=OuterRef("pk"), observation_id__isnull=True
                )
            )

            # Filter the queryset
            queryset = queryset.filter(has_dataentry_no_observation_id)

        return queryset.order_by("-entry_batch_id")

    def get_context_data(self, **kwargs):
        """
        Returns the context data for rendering the list view.

        Returns:
            dict: The context data.
        """
        context = super().get_context_data(**kwargs)
        context["persons"] = {
            person.person_id: person for person in TrtPersons.objects.all()
        }
        return context


class EntryBatchDetailView(LoginRequiredMixin, FormMixin, ListView):
    """
    A view for displaying list of a batch of TrtDataEntry objects.

    Attributes:
        model (Model): The model class for the TrtDataEntry objects.
        template_name (str): The name of the template to be used for rendering the view.
        context_object_name (str): The name of the variable to be used in the template for the queryset.
        paginate_by (int): The number of objects to display per page.

    Methods:
        get_queryset(): Returns the queryset of TrtDataEntry objects filtered by entry_batch_id.
        get_context_data(**kwargs): Returns the context data for rendering the template, including the persons dictionary.
        load_templates(): Loads the templates from the templates.json file.

    """

    model = TrtDataEntry
    template_name = "wamtram2/trtentrybatch_detail.html"
    context_object_name = "batch"
    paginate_by = 50
    form_class = TrtEntryBatchesForm
    
    def get_initial(self):
        initial = super().get_initial()
        batch_id = self.kwargs.get("batch_id")
        cookies_key_prefix = batch_id
        default_enterer = self.request.COOKIES.get(f'{cookies_key_prefix}_default_enterer')
        use_default_enterer = self.request.COOKIES.get(f'{cookies_key_prefix}_use_default_enterer', False)
        
        if default_enterer == "None" or not default_enterer:
            default_enterer = None

        if use_default_enterer and default_enterer:
            initial['entered_person_id'] = default_enterer
        
        return initial
        
    def load_templates(self):
        """
        Loads the templates from the templates.json file.
        """
        json_file_path = os.path.join(settings.BASE_DIR, 'wamtram2', 'templates.json')
        with open(json_file_path, 'r') as file:
            return json.load(file)

    def dispatch(self, request, *args, **kwargs):
        # FIXME: Permission check
        if not (
            request.user.groups.filter(name="Tagging Data Entry").exists()
            or request.user.groups.filter(name="Tagging Data Curation").exists()
            or request.user.is_superuser
        ):
            return HttpResponseForbidden(
                "You do not have permission to view this record"
            )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests.

        This method checks if a 'batch_id' is in 'kwargs'. If not, it creates a new TrtEntryBatches object
        and sets the 'batch_id' key in 'kwargs' to the newly created batch's entry_batch_id.
        Then, it calls the 'get' method of the parent class using 'super()' and returns the result.

        Args:
            request: The HTTP request object.
            args: Additional positional arguments.
            kwargs: Additional keyword arguments.

        Returns:
            The response returned by the 'get' method of the parent class.
        """
        if "batch_id" not in kwargs:
            new_batch = TrtEntryBatches.objects.create(
                pr_date_convention=False
            )  # All dates should be entered as calander dates
            self.kwargs["batch_id"] = new_batch.entry_batch_id
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """
        Returns the queryset of TrtDataEntry objects filtered by entry_batch_id.

        Returns:
            queryset (QuerySet): The filtered queryset of TrtDataEntry objects.

        """
        queryset = super().get_queryset()
        batch_id = self.kwargs.get("batch_id")

        # Check if the user has requested to filter by TrtDataEntrys with no observation_id
        if (
            "filter" in self.request.GET
            and self.request.GET["filter"] == "no_observation_id"
        ):
            # Filter the queryset
            queryset = queryset.filter(
                entry_batch_id=batch_id, observation_id__isnull=True
            )
        else:
            queryset = queryset.filter(entry_batch_id=batch_id)

        return queryset.order_by("-data_entry_id")

    def get_context_data(self, **kwargs):
        """
        Returns the context data for rendering the template, including the persons dictionary.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            context (dict): The context data for rendering the template.

        """
        context = super().get_context_data(**kwargs)
        context["persons"] = {
            person.person_id: person for person in TrtPersons.objects.all()
        }

        batch = TrtEntryBatches.objects.get(entry_batch_id=self.kwargs.get("batch_id"))
        context["batch"] = batch  # add the batch to the context
        initial = self.get_initial()
        context["form"] = TrtEntryBatchesForm(
            instance=batch,
            initial=initial
        )  # Add the form to the context data
        
        # Add the templates to the context data
        cookies_key_prefix = self.kwargs.get("batch_id")
        context['selected_template'] = self.request.COOKIES.get(f'{cookies_key_prefix}_selected_template', '')
        context['use_default_enterer'] = self.request.COOKIES.get(f'{cookies_key_prefix}_use_default_enterer', False)
        context['default_enterer'] = self.request.COOKIES.get(f'{cookies_key_prefix}_default_enterer', None)

        context['cookies_key_prefix'] = cookies_key_prefix
        context['default_enterer_value'] = context['default_enterer']
        context['templates'] = self.load_templates()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form.instance.entry_batch_id = self.kwargs.get("batch_id")
        if form.is_valid():
            batch = form.save()
            result = self.form_valid(form)
            batch_id = self.kwargs.get("batch_id")
            cookies_key_prefix = batch_id
            response = result
            response.set_cookie(f'{cookies_key_prefix}_selected_template', request.POST.get('selected_template'), max_age=3600)
            response.set_cookie(f'{cookies_key_prefix}_use_default_enterer', request.POST.get('use_default_enterer') == 'on', max_age=3600)
            response.set_cookie(f'{cookies_key_prefix}_default_enterer', batch.entered_person_id.person_id if batch.entered_person_id else None, max_age=3600)

            return result
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        batch = form.save(commit=False)

        batch_id = batch.entry_batch_id

        # Get the existing instance from the database
        existing_batch = TrtEntryBatches.objects.get(entry_batch_id=batch_id)

        # Update the PR_DATE_CONVENTION field with the existing value
        if 'pr_date_convention' not in form.cleaned_data:
            batch.pr_date_convention = existing_batch.pr_date_convention
        batch.entry_date = existing_batch.entry_date
        batch.filename = existing_batch.filename

        # Save the batch instance
        batch.save()

        # Redirect to the success URL
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        batch_id = self.kwargs.get("batch_id")
        return reverse("wamtram2:entry_batch_detail", args=[batch_id])


class TrtDataEntryFormView(LoginRequiredMixin, FormView):
    """
    A form view for entering TRT data.
    """

    template_name = "wamtram2/trtdataentry_form.html"
    form_class = TrtDataEntryForm

    def dispatch(self, request, *args, **kwargs):
        # FIXME: Permission check
        if not (
            request.user.groups.filter(name="Tagging Data Entry").exists()
            or request.user.groups.filter(name="Tagging Data Curation").exists()
            or request.user.is_superuser
        ):
            return HttpResponseForbidden(
                "You do not have permission to view this record"
            )
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.

        If an entry_id is provided in the URL, retrieves the corresponding TrtDataEntry instance
        and adds it as the 'instance' argument in the form kwargs. If no entry_id is provided,
        a new, blank form is instantiated.

        Returns:
            dict: The keyword arguments for instantiating the form.
        """
        kwargs = super().get_form_kwargs()
        entry_id = self.kwargs.get("entry_id")
        if entry_id:
            entry = get_object_or_404(TrtDataEntry.objects.select_related('turtle_id'), data_entry_id=entry_id)
            kwargs["instance"] = entry

        return kwargs
    
    def get_template_data(self, template_key):
        json_file_path = os.path.join(settings.BASE_DIR, 'wamtram2', 'templates.json')
        with open(json_file_path, 'r') as file:
            templates = json.load(file)
        return templates.get(template_key)

    def get_initial(self):
        initial = super().get_initial()
        batch_id = self.kwargs.get("batch_id")
        turtle_id = self.kwargs.get("turtle_id")
        entry_id = self.kwargs.get("entry_id")
        
        cookies_key_prefix = batch_id

        selected_template = self.request.COOKIES.get(f'{cookies_key_prefix}_selected_template')
        use_default_enterer = self.request.COOKIES.get(f'{cookies_key_prefix}_use_default_enterer', False)
        default_enterer = self.request.COOKIES.get(f'{cookies_key_prefix}_default_enterer', None)
        
        if default_enterer == "None" or not default_enterer:
            default_enterer = None

        # If a template is selected, populate the form with the template data
        if selected_template:
            template_data = self.get_template_data(selected_template)
            if template_data:
                initial['place_code'] = template_data.get('place_code')
                # Only set species_code and sex from template if turtle_id is not present
                if not turtle_id:
                    initial['species_code'] = template_data.get('species_code')
                    initial['sex'] = template_data.get('sex')
                    
        if batch_id:
            initial["entry_batch"] = get_object_or_404(TrtEntryBatches, entry_batch_id=batch_id)
            if use_default_enterer and default_enterer:
                initial['entered_by_id'] = default_enterer

        if turtle_id:
            turtle = get_object_or_404(TrtTurtles.objects.prefetch_related('trttags_set', 'trtpittags_set'), pk=turtle_id)
            initial["turtle_id"] = turtle_id
            initial["species_code"] = turtle.species_code
            initial["sex"] = turtle.sex
        
        # editing an existing observation we need to populate the person id fields from the strings stored
        # using the old MS Access system
        
        if entry_id:
            trtdataentry = get_object_or_404(TrtDataEntry, data_entry_id=entry_id)
            measured_by = trtdataentry.measured_by
            recorded_by = trtdataentry.recorded_by
            tagged_by = trtdataentry.tagged_by
            entered_by = trtdataentry.entered_by
            measured_recorded_by = trtdataentry.measured_recorded_by

            if measured_by:
                first_name, last_name = measured_by.split(" ")
                person = TrtPersons.objects.filter(
                    first_name=first_name, surname=last_name
                ).first()
                if person:
                    initial["measured_by_id"] = person.person_id
            if recorded_by:
                first_name, last_name = recorded_by.split(" ")
                person = TrtPersons.objects.filter(
                    first_name=first_name, surname=last_name
                ).first()
                if person:
                    initial["recorded_by_id"] = person.person_id
            if tagged_by:
                first_name, last_name = tagged_by.split(" ")
                person = TrtPersons.objects.filter(
                    first_name=first_name, surname=last_name
                ).first()
                if person:
                    initial["tagged_by_id"] = person.person_id
            if entered_by:
                first_name, last_name = entered_by.split(" ")
                person = TrtPersons.objects.filter(
                    first_name=first_name, surname=last_name
                ).first()
                if person:
                    initial["entered_by_id"] = person.person_id
            if measured_recorded_by:
                first_name, last_name = measured_recorded_by.split(" ")
                person = TrtPersons.objects.filter(
                    first_name=first_name, surname=last_name
                ).first()
                if person:
                    initial["measured_recorded_by_id"] = person.person_id

        return initial

    def form_valid(self, form):
        """
        Saves the form and returns the success URL.

        Args:
            form (Form): The form instance.

        Returns:
            str: The success URL.
        """
        # instance = form.save(commit=False)
        # if 'turtle_id' in self.kwargs:
        #     instance.turtle_id = TrtTurtles.objects.get(turtle_id=self.kwargs['turtle_id'])
        #     instance.save()
        # form.save_tag_info(instance) 
        form.save()
        # Get the batch_id
        batch_id = form.cleaned_data["entry_batch"].entry_batch_id

        # Set the success URL
        self.success_url = reverse("wamtram2:entry_batch_detail", args=[batch_id])

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Returns the context data for rendering the template.

        Adds the entry_id and entry objects to the context.

        Returns:
            dict: The context data.
        """
        context = super().get_context_data(**kwargs)
        entry_id = self.kwargs.get("entry_id")
        batch_id = self.kwargs.get("batch_id")
        cookies_key_prefix = batch_id
        if entry_id:
            context["entry_id"] = entry_id  # Editing existing entry
            context["entry"] = get_object_or_404(TrtDataEntry.objects.select_related('turtle_id'), data_entry_id=entry_id)
        if batch_id:
            context["batch_id"] = batch_id  # Creating new entry in batch
            context["selected_template"] = self.request.COOKIES.get(f'{cookies_key_prefix}_selected_template')
            context["use_default_enterer"] = self.request.COOKIES.get(f'{cookies_key_prefix}_use_default_enterer', False)
            context["default_enterer"] = self.request.COOKIES.get(f'{cookies_key_prefix}_default_enterer', None)

        return context


class DeleteBatchView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        # FIXME: Permission check
        if not (
            request.user.groups.filter(name="Tagging Data Entry").exists()
            or request.user.groups.filter(name="Tagging Data Curation").exists()
            or request.user.is_superuser
        ):
            return HttpResponseForbidden(
                "You do not have permission to view this record"
            )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, batch_id):
        batch = get_object_or_404(TrtEntryBatches, entry_batch_id=batch_id)
        batch.delete()
        return redirect("wamtram2:entry_batches")


class ValidateDataEntryBatchView(LoginRequiredMixin, View):
    """
    View class for validating a data entry batch.

    This view executes a stored procedure to validate the data in a batch
    identified by the 'batch_id' parameter. If the validation is successful,
    a success message is added to the request's messages framework. If there
    is a database error, an error message is added instead.

    After the validation, the view redirects to the 'entry_batch_detail' view
    with the 'batch_id' parameter.

    Attributes:
        - request: The HTTP request object.
        - args: Additional positional arguments passed to the view.
        - kwargs: Additional keyword arguments passed to the view.
    """

    def dispatch(self, request, *args, **kwargs):
        # FIXME: Permission check
        if not (
            request.user.groups.filter(name="Tagging Data Entry").exists()
            or request.user.groups.filter(name="Tagging Data Curation").exists()
            or request.user.is_superuser
        ):
            return HttpResponseForbidden(
                "You do not have permission to view this record"
            )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            with connections["wamtram2"].cursor() as cursor:
                cursor.execute(
                    "EXEC dbo.ValidateDataEntryBatch @ENTRY_BATCH_ID = %s",
                    [self.kwargs["batch_id"]],
                )
                messages.add_message(request, messages.INFO, "Validation finished.")
        except DatabaseError as e:
            messages.add_message(
                request, messages.ERROR, "Database error: {}".format(e)
            )
        return redirect("wamtram2:entry_batch_detail", batch_id=self.kwargs["batch_id"])


class ProcessDataEntryBatchView(LoginRequiredMixin, View):
    """
    View class for processing a data entry batch.

    This view executes a stored procedure to process a data entry batch
    identified by the batch ID provided in the URL parameters. It uses the
    'wamtram2' database connection and redirects the user to the detail page
    of the processed batch.

    Attributes:
        None

    Methods:
        get: Handles the GET request and executes the stored procedure.

    Raises:
        DatabaseError: If there is an error executing the stored procedure.

    Returns:
        HttpResponseRedirect: Redirects the user to the detail page of the
        processed batch.
    """

    def dispatch(self, request, *args, **kwargs):
        # FIXME: Permission check
        if not (
            request.user.groups.filter(name="Tagging Data Entry").exists()
            or request.user.groups.filter(name="Tagging Data Curation").exists()
            or request.user.is_superuser
        ):
            return HttpResponseForbidden(
                "You do not have permission to view this record"
            )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            with connections["wamtram2"].cursor() as cursor:
                cursor.execute(
                    "EXEC dbo.EntryBatchProcess @ENTRY_BATCH_ID = %s;",
                    [self.kwargs["batch_id"]],
                )
                messages.add_message(request, messages.INFO, "Processing finished.")
        except DatabaseError as e:
            messages.add_message(
                request, messages.ERROR, "Database error: {}".format(e)
            )
        return redirect("wamtram2:entry_batch_detail", batch_id=self.kwargs["batch_id"])


class FindTurtleView(LoginRequiredMixin, View):
    """
    View class for finding a turtle based on tag and pit tag ID.
    """

    def dispatch(self, request, *args, **kwargs):
        # FIXME: Permission check
        if not (
            request.user.groups.filter(name="Tagging Data Entry").exists()
            or request.user.groups.filter(name="Tagging Data Curation").exists()
            or request.user.is_superuser
        ):
            return HttpResponseForbidden(
                "You do not have permission to view this record"
            )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        batch_id = kwargs.get("batch_id")

        form = SearchForm(initial={
            "batch_id": batch_id,
        })
        return render(request, "wamtram2/find_turtle.html", {"form": form})
    def post(self, request, *args, **kwargs):
        batch_id = kwargs.get("batch_id")
        form = SearchForm(request.POST, initial={"batch_id": batch_id})
        no_turtle_found = False # Flag to indicate if no turtle was found

        if form.is_valid():
            tag_id = form.cleaned_data["tag_id"]
            turtle = None

            try:
                # Check if the tag is a turtle tag or a pit tag
                tag = TrtTags.objects.select_related('turtle').filter(tag_id=tag_id).first()
                if tag:
                    turtle = tag.turtle
                else:
                    pit_tag = TrtPitTags.objects.select_related('turtle').filter(pittag_id=tag_id).first()
                    if pit_tag:
                        turtle = pit_tag.turtle

                if turtle:
                    # Prefetch related tags and pit tags
                    turtle = TrtTurtles.objects.prefetch_related('trttags_set', 'trtpittags_set').get(pk=turtle.pk)
                    return render(
                        request,
                        "wamtram2/find_turtle.html",
                        {
                            "form": form,
                            "turtle": turtle,
                            "tags": turtle.trttags_set.all(),
                            "pittags": turtle.trtpittags_set.all(),
                        },
                    )
                else:
                    raise TrtTags.DoesNotExist

            except TrtTags.DoesNotExist:
                form.add_error(None, "No Turtle found with the given tag id.")
                no_turtle_found = True

        return render(
            request,
            "wamtram2/find_turtle.html",
            {"form": form, "no_turtle_found": no_turtle_found},
        )


class ObservationDetailView(LoginRequiredMixin, DetailView):
    model = TrtObservations
    template_name = "wamtram2/observation_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = get_object_or_404(TrtObservations, observation_id=self.kwargs.get("pk"))
        context["observation"] = obj
        context["tags"] = obj.trtrecordedtags_set.all()
        context["pittags"] = obj.trtrecordedpittags_set.all()
        context["measurements"] = obj.trtmeasurements_set.all()
        return context


class TurtleListView(LoginRequiredMixin, PaginateMixin, ListView):
    """
    View class for displaying a list of turtles.

    Attributes:
        model (Model): The model class representing the turtles.
        paginate_by (int): The number of turtles to display per page.
    """

    model = TrtTurtles
    paginate_by = 50

    def get_context_data(self, **kwargs):
        """
        Retrieves the context data for rendering the template.

        Returns:
            dict: The context data.
        """
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"{settings.SITE_CODE} | WAMTRAM2"
        # Pass in any query string
        if "q" in self.request.GET:
            context["query_string"] = self.request.GET["q"]
        context["breadcrumbs"] = (
            Breadcrumb("Home", reverse("home")),
            Breadcrumb("Tagged turtles", None),
        )
        return context

    def get_queryset(self):
        """
        Retrieves the queryset of turtles to be displayed.

        Returns:
            QuerySet: The queryset of turtles.
        """
        qs = super().get_queryset()
        # General-purpose search uses the `q` parameter.
        if "q" in self.request.GET and self.request.GET["q"]:
            q = self.request.GET["q"]
            qs = qs.filter(
                Q(pk__icontains=q)
                | Q(trttags__tag_id__icontains=q)
                | Q(trtpittags__pittag_id__icontains=q)
            ).distinct()

        return qs.order_by("pk")


class TurtleDetailView(LoginRequiredMixin, DetailView):
    """
    View class for displaying the details of a turtle.

    Attributes:
        model (Model): The model class representing the turtle.
    """

    model = TrtTurtles

    def get_context_data(self, **kwargs):
        """
        Retrieves the context data for rendering the template.

        Returns:
            dict: The context data.
        """
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context["page_title"] = f"{settings.SITE_CODE} | WAMTRAM2 | {obj.pk}"
        context["tags"] = obj.trttags_set.all()
        context["pittags"] = obj.trtpittags_set.all()
        context["observations"] = obj.trtobservations_set.all()
        return context


SEX_CHOICES = [
    ("M", "Male"),
    ("F", "Female"),
    ("I", "Indeterminate"),
]
class TemplateManageView(View):

    def get_json_path(self):
        return os.path.join(settings.BASE_DIR, 'wamtram2', 'templates.json')

    def load_templates_from_json(self):
        try:
            with open(self.get_json_path(), 'r') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError as e:
            # Log error and return empty dictionary
            print(f"Error decoding JSON: {e}")
            return {}

    def save_templates_to_json(self, templates):
        try:
            with open(self.get_json_path(), 'w') as file:
                json.dump(templates, file, indent=4)
        except IOError as e:
            print(f"Error writing to JSON file: {e}")
            raise

    def get_next_template_key(self, templates):
        max_key = 0
        template_key_pattern = re.compile(r'^template(\d+)$')
        for key in templates.keys():
            match = template_key_pattern.match(key)
            if match:
                max_key = max(max_key, int(match.group(1)))
        return f"template{max_key + 1}"

    def get(self, request):
        templates = self.load_templates_from_json()
        form = TemplateForm()
        places = list(TrtPlaces.objects.all())
        species = list(TrtSpecies.objects.all())
        return render(request, 'wamtram2/template_manage.html', {
            'templates': templates, 
            'form': form, 
            'places': places, 
            'species': species,
            'sex_choices': SEX_CHOICES
        })

    def post(self, request):
        form = TemplateForm(request.POST)
        if form.is_valid():
            new_template = form.save(commit=False)
            templates = self.load_templates_from_json()
            new_template_data = {
                'name': new_template.name,
                'place_code': request.POST.get('place_code'),
                'species_code': request.POST.get('species_code'),
                'sex': request.POST.get('sex')
            }
            template_key = self.get_next_template_key(templates)
            templates[template_key] = new_template_data
            try:
                self.save_templates_to_json(templates)
                return redirect('wamtram2:template_manage')
            except Exception as e:
                return render(request, 'wamtram2/template_manage.html', {
                    'form': form,
                    'templates': templates,
                    'places': list(TrtPlaces.objects.all()), 
                    'species': list(TrtSpecies.objects.all()),
                    'sex_choices': SEX_CHOICES,
                    'error_message': f"Error saving template: {e}"
                })
        else:
            return render(request, 'wamtram2/template_manage.html', {
                'form': form, 
                'templates': self.load_templates_from_json(), 
                'places': list(TrtPlaces.objects.all()), 
                'species': list(TrtSpecies.objects.all()),
                'sex_choices': SEX_CHOICES,
                'error_message': "Invalid form data. Please correct the errors below."
            })

    def put(self, request, template_key):
        templates = self.load_templates_from_json()
        template_data = templates.get(template_key)
        if not template_data:
            return JsonResponse({'error': 'Template not found'}, status=404)

        put_data = QueryDict(request.body)
        
        template_instance = Template(
            name=template_data['name'],
            place_code=template_data['place_code'],
            species_code=template_data['species_code'],
            sex=template_data['sex']
        )
        
        form = TemplateForm(put_data, instance=template_instance)
        if form.is_valid():
            updated_template = form.save(commit=False)
            updated_template_data = {
                'name': updated_template.name,
                'place_code': put_data.get('place_code'),
                'species_code': put_data.get('species_code'),
                'sex': put_data.get('sex')
            }
            templates[template_key] = updated_template_data
            try:
                self.save_templates_to_json(templates)
                return JsonResponse(updated_template_data)
            except Exception as e:
                return JsonResponse({'error': f"Error saving template: {e}"}, status=500)
        return JsonResponse({'errors': form.errors}, status=400)

    def delete(self, request, template_key):
        templates = self.load_templates_from_json()
        if template_key in templates:
            del templates[template_key]
            try:
                self.save_templates_to_json(templates)
                return JsonResponse({'message': 'Template deleted'})
            except Exception as e:
                return JsonResponse({'error': f"Error deleting template: {e}"}, status=500)
        return JsonResponse({'error': 'Template not found'}, status=404)

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return self.put(request, *args, **kwargs)
        elif request.method == 'DELETE':
            return self.delete(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)
    

def validate_turtle_tag(request):
    """
    Validates if a given tag matches the turtle ID.

    This method retrieves the turtle ID and tag from the GET parameters and checks 
    if the tag belongs to the specified turtle. It returns a JSON response indicating 
    whether the tag is valid for the turtle.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response containing the validation result. The response 
                    includes a 'valid' key with a boolean value indicating if the 
                    tag is valid, and a 'message' key with an error message if applicable.

    Example:
        GET /validate-turtle-tag?turtle_id=1&tag=1234

        Response:
        {
            "valid": true
        }
    """
    turtle_id = request.GET.get('turtle_id')
    tag = request.GET.get('tag')
    
    if not turtle_id or not tag:
        return JsonResponse({'valid': False, 'message': 'Missing parameters'})

    try:
        turtle = TrtTurtles.objects.get(turtle_id=turtle_id)
        is_valid = turtle.trttags_set.filter(tag_id=tag).exists()
        return JsonResponse({'valid': is_valid})
    except TrtTurtles.DoesNotExist:
        return JsonResponse({'valid': False, 'message': 'Turtle not found'})    


