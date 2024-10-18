from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .models import Incident, Uploaded_file
from .forms import IncidentForm, UploadedFileForm
from django.contrib import messages
from django.db import transaction 


# def create_incident(request):
#     UploadedFileFormSet = inlineformset_factory(
#         Incident, 
#         Uploaded_file, 
#         form=UploadedFileForm, 
#         extra=1, 
#         can_delete=False
#     )
    
#     if request.method == 'POST':
#         form = IncidentForm(request.POST)
#         formset = UploadedFileFormSet(request.POST, request.FILES)
#         if form.is_valid() and formset.is_valid():
#             incident = form.save()
#             print(f"Incident created: {incident.id}")
#             formset.instance = incident
#             formset.save()
#             messages.success(request, 'Incident created successfully')
#             return redirect('marine_mammal_incidents:incident_list')
#         else:
#             print(form.errors)
#             print(formset.errors)
#             messages.error(request, 'Error creating incident. Please check the form.')
#     else:
#         form = IncidentForm()
#         formset = UploadedFileFormSet()
    
#     context = {
#         'form': form,
#         'formset': formset,
#     }
#     return render(request, 'marine_mammal_incidents/create_incident.html', context)

import logging
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.db import transaction
from .models import Incident, Uploaded_file
from .forms import IncidentForm, UploadedFileForm
from django.contrib import messages


logger = logging.getLogger(__name__)

@transaction.atomic 
def create_incident(request):

    UploadedFileFormSet = inlineformset_factory(
        Incident, 
        Uploaded_file, 
        form=UploadedFileForm, 
        extra=1, 
        can_delete=False
    )

    if request.method == 'POST':
        form = IncidentForm(request.POST)
        formset = UploadedFileFormSet(request.POST, request.FILES)
        
        if form.is_valid() and formset.is_valid():
            try:
                incident = form.save()
                logger.info(f"Incident created: ID = {incident.id}, Data = {incident.__dict__}")
                
                formset.instance = incident
                formset.save()
                logger.info(f"Uploaded files saved for Incident ID = {incident.id}")
                
                messages.success(request, 'Incident created successfully')
                
                return redirect('marine_mammal_incidents:incident_list')
            
            except Exception as e:
                logger.exception(f"Error occurred while saving the incident: {e}")
                messages.error(request, f"Error creating incident: {e}")
        
        else:
            logger.error(f"Form errors: {form.errors}")
            logger.error(f"Formset errors: {formset.errors}")
            messages.error(request, 'Error creating incident. Please check the form.')

    else:
        form = IncidentForm()
        formset = UploadedFileFormSet()
    
    logger.info("Rendering incident creation form")

    context = {
        'form': form,
        'formset': formset,
    }

    return render(request, 'marine_mammal_incidents/create_incident.html', context)

def incident_list(request):
    incidents = Incident.objects.all().order_by('-incident_date')
    context = {
        'incidents': incidents,
    }
    return render(request, 'marine_mammal_incidents/incident_list.html', context)