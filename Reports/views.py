from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from Reports.forms import reportForm
from Questions.models import *
from Locations.models import *

# Create your views here.
def chooseLocation(request):
    if request.method == 'POST':
        form = reportForm(request.POST)
        if form.is_valid():
            clusterID = form.cleaned_data['cluster']
            print(type(clusterID))
            return redirect('qnn/%s' % clusterID)

    form = reportForm()
    context={
        "form": form
    }
    return render(request, 'reports-location.html', context)

def chooseQuestionnaire(request, clusterID):
    if request.method == 'POST':
        questionnaireID = request.POST['qnn-btn']
        return redirect('%s/' % questionnaireID)
    distinct_qnn = []
    nondistinct_qnn = PatientAssessment.objects.filter(assess_patientID__householdID__parentLocID = int(clusterID)).exclude(assess_questionnaireID__questionnaireName__icontains='household').values('assess_questionnaireID')
    for item in nondistinct_qnn:
        if item['assess_questionnaireID'] not in distinct_qnn:
            distinct_qnn.append(item['assess_questionnaireID'])
    questionnaires = []
    for item in distinct_qnn:
        try:
            qnn = get_object_or_404(Questionnaire, pk=item)
            questionnaires.append(qnn)    
        except ObjectDoesNotExist:
             continue
    context ={
        "questionnaires": questionnaires
    }
    return render(request, 'reports-qnn.html', context)

def reportQnn(request, clusterID, questionnaireID):
    data = []
    questionnaire = Questionnaire.objects.get(pk=questionnaireID)
    location = Location.objects.get(pk=clusterID)
    questions = Questions.objects.filter(questionnaireID=questionnaireID).order_by('questionID').values()
    for question in questions:
        questionString = question['questionString']
        questionID = question['questionID']
        QA_objects = QuestionAnswer.objects.filter(questionnaireID=questionnaireID, questionID=questionID).select_related('answerID')
        associated_answers = []
        associated_response_number = []
        for answer in QA_objects:
            associated_answers.append(answer.answerID.answerString)
            response = QuestionResponse.objects.filter(questionnaireID=questionnaireID, questionID=questionID, answerID=answer.answerID.answerID).count()
            associated_response_number.append(str(response))
        
        string_answers = '$#'.join(associated_answers)
        string_response = '$#'.join(associated_response_number)
        data_dict = {
            "questionString": questionString,
            "questionID": questionID, 
            "answer_list": string_answers,
            "response_list": string_response
        }
        data.append(data_dict)   
    context = {
        "data": data,
        "questionnaire": questionnaire.questionnaireName,
        "country": location.parentLocID.parentLocID.locationName,
        "region": location.parentLocID.locationName,
        "cluster": location.locationName
    }
    return render(request, 'reports-questions.html', context)