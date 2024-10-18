from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .models import Incident, Uploaded_file
from .forms import IncidentForm, UploadedFileForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.views.generic import ListView


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
            incident = form.save()
            print(f"Incident created: {incident.id}")
            formset.instance = incident
            formset.save()
            messages.success(request, 'Incident created successfully')
            return redirect('marine_mammal_incidents:incident_list')
        else:
            print(form.errors)
            print(formset.errors)
            messages.error(request, 'Error creating incident. Please check the form.')
    else:
        form = IncidentForm()
        formset = UploadedFileFormSet()
    
    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'marine_mammal_incidents/create_incident.html', context)


def incident_list(request):
    incidents = Incident.objects.all().order_by('-incident_date')
    
    paginator = Paginator(incidents, 3) 
    page = request.GET.get('page')
    
    try:
        incidents = paginator.page(page)
    except PageNotAnInteger:
        incidents = paginator.page(1)
    except EmptyPage:
        incidents = paginator.page(paginator.num_pages)
    
    context = {
        'incidents': incidents,
        'object_count': paginator.count,
        'is_paginated': incidents.has_other_pages(),
    }
    return render(request, 'marine_mammal_incidents/incident_list.html', context)