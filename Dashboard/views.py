from django.shortcuts import render
from django.template import loader
from django.http import JsonResponse
from .forms import *
from Questions import models
from Locations import models
from API import serializers
from django.forms.models import model_to_dict

def DashboardView(request):
    form = dashboardForm()

    incomplete = PatientAssessment.objects.filter(questionnaireStatus = "INCOMPLETE").count()
    incomplete_patients = PatientAssessment.objects.filter(questionnaireStatus = "INCOMPLETE").values()
    complete = PatientAssessment.objects.filter(questionnaireStatus = "COMPLETE").count()
    sizes = [complete, incomplete]
    labels = ['Completed Assessment', 'Unfinished Assessment']
    context = {
        'form': form,
        'sizes': sizes,
        'labels': labels,
        'incomplete_patients': incomplete_patients,
    }
    return render(request, 'dashboard.html', context)

def ajaxLocation(request):
    locations_to_render = []
    location_id = request.GET.get('location_id')
    location_type = request.GET.get('location_type')
    query_locations = Location.objects.filter(parentLocID = location_id)
    for loc in query_locations:
        locations_to_render.append(str(loc.locationID))
    return JsonResponse({'locations': locations_to_render})

def ajaxData(request):
    countryID = request.GET.get('countryID')
    regionID = request.GET.get('regionID')
    clusterID = request.GET.get('clusterID')
    if clusterID != '0':
        incomplete = PatientAssessment.objects.filter(
            questionnaireStatus = "INCOMPLETE", 
            assess_patientID__householdID__parentLocID = int(clusterID)).count()
        complete = PatientAssessment.objects.filter(
            questionnaireStatus = "COMPLETE",
            assess_patientID__householdID__parentLocID = int(clusterID)).count()
    elif regionID != '0':
        incomplete = PatientAssessment.objects.filter(
            questionnaireStatus = "INCOMPLETE",
            assess_patientID__householdID__parentLocID__parentLocID = int(regionID)).count()
        complete = PatientAssessment.objects.filter(
            questionnaireStatus = "COMPLETE",
            assess_patientID__householdID__parentLocID__parentLocID = int(regionID)).count()       
    elif countryID != '0':
        incomplete = PatientAssessment.objects.filter(
            questionnaireStatus = "INCOMPLETE",
            assess_patientID__householdID__parentLocID__parentLocID__parentLocID = int(countryID)).count()
        complete = PatientAssessment.objects.filter(
            questionnaireStatus = "COMPLETE",
            assess_patientID__householdID__parentLocID__parentLocID__parentLocID = int(countryID)).count()
    elif countryID == '0':
        incomplete = PatientAssessment.objects.filter(questionnaireStatus = "INCOMPLETE").count()
        complete = PatientAssessment.objects.filter(questionnaireStatus = "COMPLETE").count() 
    return JsonResponse({'data': [complete, incomplete]})

def ajaxIncompletePatients(request):
    countryID = request.GET.get('countryID')
    regionID = request.GET.get('regionID')
    clusterID = request.GET.get('clusterID')
    if clusterID != '0':
        incomplete_patients = PatientAssessment.objects.filter(
            questionnaireStatus = "INCOMPLETE", 
            assess_patientID__householdID__parentLocID = int(clusterID)).values()
    elif regionID != '0':
        incomplete_patients = PatientAssessment.objects.filter(
            questionnaireStatus = "INCOMPLETE",
            assess_patientID__householdID__parentLocID__parentLocID = int(regionID)).values()
    elif countryID != '0':
        incomplete_patients = PatientAssessment.objects.filter(
                    questionnaireStatus = "INCOMPLETE",
                    assess_patientID__householdID__parentLocID__parentLocID__parentLocID = int(countryID)).values()
    elif countryID == '0':
        incomplete_patients = PatientAssessment.objects.filter(questionnaireStatus = "INCOMPLETE").select_related()
    data = []
    for patient in incomplete_patients:
        
        data.append({
            'patient_id' : patient.assess_patientID.patientID,
            'questionnaire_id': patient.assess_questionnaireID.questionnaireID,
            'questionnaire_name': patient.assess_questionnaireID.questionnaireName,
            'start': patient.start
        })
        # data.append({
        #     'patient_id' : patient['assess_patientID_id'],
        #     'questionnaire_id': patient['assess_questionnaireID_id'],
        #     'start': patient['start']
        # })
        # print(patient.assess_questionnaireID.questionnaireName)
        # print(patient.assess_patientID)

    return JsonResponse({'data':data})