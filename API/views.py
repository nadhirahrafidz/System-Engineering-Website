from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from Locations.models import Location
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from API.serializers import *

"""
API's used to sync table information from server database to mobile application. Only GET or POST (or both) requests are 
made available for each table. No deletion of data is allowed. 

Authentication token is required to be provided in the header in this form:
Key: Authorization
Value: Token {{Token}}

Content type is required to be provided in the header in this form:
Key: Content-type
Value: application/json

"""


"""
Database table: mobility.locations_location
Django Model: Locations.Location
Endpoint: /tables/Location

GET Request: returns LIST of all locations in server database 
"""
class LocationTable(APIView):
    def get(self, request):
        data = Location.objects.all()
        serializer = LocationSerializer(data, many=True)
        return Response(serializer.data)

"""
Database table: mobility.questions_questionnaire
Django Model: Questions.Questionnaire
Endpoint: /tables/Questionnaire

GET Request: returns LIST of all questionnaires in server database 
Table Fields: questionnaireID, questionnaireName, questionnaireVersion
"""
class QuestionnaireTable(APIView):
    def get(self, request):
        data = Questionnaire.objects.all()
        serializer = QuestionnaireSerializer(data, many=True)
        return Response(serializer.data)

"""
Database table: mobility.questions_questions
Django Model: Questions.Questions
Endpoint: /tables/Questions

GET Request: returns LIST of all questions that belong to questionnaires that are ACTIVE (Questionnaire's active_flag = 1)
Returned Fields: questionID, questionString, answerMin, answerMax, questionInstruction, questionMedia, questionTypeID, questionnaireID
"""
class QuestionTable(APIView):
    def get(self, request):
        # Exception of no data found
        data = Questions.objects.filter(questionnaireID__active_flag=1)
        serializer = QuestionSerializer(data, many=True)
        return Response(serializer.data)

"""
Database table: mobility.questions_answer
Django Model: Questions.Answer
Endpoint: /tables/Answers

GET Request: returns LIST of all answers that belong to questionnaires that are ACTIVE (Questionnaire's active_flag = 1)
Returned Fields: questionID, answerID, questionnaireID
"""
class AnswerTable(APIView):
    def get(self, request):
        # Exception of no data found
        data = Answer.objects.filter(questionnaireID__active_flag=1)
        serializer = AnswerSerializer(data, many=True)
        return Response(serializer.data)


"""
Database table: mobility.questions_questionanswer
Django Model: Questions.QuestionAnswer
Endpoint: /tables/QuestionAnswer

GET Request: returns LIST of all questions and its related answer(s) from questionnaires that are ACTIVE (Questionnaire's active_flag = 1)
Returned fields: questionID, questionString, answerMin, answerMax, questionInstruction, questionMedia, questionTypeID, questionnaireID
"""
class QuestionAnswerTable(APIView):
    def get(self, request):
        # Exception of no data found
        data = QuestionAnswer.objects.filter(questionnaireID__active_flag=1)
        serializer = QuestionAnswerSerializer(data, many=True)
        return Response(serializer.data)

"""
Database table: mobility.questions_logic
Django Model: Questions.Logic
Endpoint: /tables/Logic

GET Request: returns LIST of all Logic Table entries where questionnaire is active 
Returned fields: seq_num, logic_questionID, rel_ans_ID, next_qID, rel_type, rel_ID, questionnaireID
"""
class LogicTable(APIView):
    def get(self, request):
        # Exception of no data found
        data = Logic.objects.filter(questionnaireID__active_flag=1)
        serializer = LogicSerializer(data, many=True)
        return Response(serializer.data)

"""
Database table: mobility.questionsrelation
Django Model: Questions.QuestionRelation
Endpoint: /tables/Logic

GET Request: returns LIST of all QuestionRelation Table entries whose questionnaire is active 
Returned fields: question_rel_questionID, questionnaireID, rel_ID, rel_ans_ID, rel_qID
"""
class QRelTable(APIView):
    def get(self, request):
        # Exception of no data found
        data = QuestionRelation.objects.filter(questionnaireID__active_flag=1)
        serializer = QRelSerializer(data, many=True)
        return Response(serializer.data)

"""
Database table: mobility.patients_patient
Django Model: Patients.Patient
Endpoint: /tables/Patients

GET Request: returns LIST of all Patients Table entries within a certain Cluster Location
Returned fields: patientID, studyID, date_of_birth, prefix, firstName, middleName, lastName, suffix, com_name, gender, dur_hh, exam_status, 
notes, lvl_edu, work_status, marital_status, motherFirstName, motherLastName, tel1_num, tel1_owner, tel1_owner_rel, tel2_num, tel2_owner, 
tel2_owner_rel, nationalID, deceased, deceased_date, responder, proxy_rel, enumeratorID, householdID

Body parameters: clusterID - cluster in which the patient's householdID is registered under (household's parentLocID)
Key: clusterID
Example: 
{
    "clusterID":"33"
}
"""
class PatientTable(APIView):
    def get(self, request):
        location = request.GET.get("clusterID")
        # Exception of no data found
        data = Patient.objects.filter(householdID__parentLocID = location)
        serializer = PatientSerializer(data, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        results = []
        for patient in data['data']:
            print(patient)
            # print(patient['enumeratorID'])
            # print(type(patient['enumeratorID']))
            enumerator = get_object_or_404(Enumerator, enumeratorID=patient['enumeratorID'])
            household = get_object_or_404(HouseHold, householdID=patient['householdID'])
            patient, created = Patient.objects.get_or_create(
                patientID=patient['patientID'],
                studyID=patient['studyID'],
                date_of_birth=patient['date_of_birth'],
                prefix=patient['prefix'],
                firstName=patient['first_name'],
                middleName=patient['middle_name'],
                lastName=patient['last_name'],
                suffix=patient['suffix'],
                com_name=patient['com_name'],
                gender=patient['gender'],
                householdID=household, 
                dur_hh=patient['dur_hh'],
                notes=patient['notes'],
                lvl_edu=patient['lvl_edu'],
                work_status=patient['work_status'],
                marital_status=patient['marital_status'],
                motherFirstName=patient['mother_first_name'],
                motherLastName=patient['mother_last_name'],
                tel1_num=patient['tel1_num'],
                tel1_owner=patient['tel1_owner'],
                tel1_owner_rel=patient['tel1_owner_rel'],
                tel2_num=patient['tel2_num'],
                tel2_owner=patient['tel2_owner'],
                tel2_owner_rel=patient['tel2_owner_rel'],
                enumeratorID=enumerator,
                nationalID=patient['national_id'],
                deceased=patient['deceased'],
                deceased_date=patient['deceased_date'],
                responder=patient['responder'],
                proxy_name=patient['proxy_name'],
                proxy_rel=patient['proxy_rel']
            )
            if created == False:
                print("exists")
                # patient.save()
            results.append(Patient.objects.get(patientID=patient.patientID))
        serializer = PatientSerializer(results, many=True)
        return Response(serializer.data)      

"""
Database table: mobility.questions_patientassessment 
Django Model: Questions.PatientAssessment
Endpoint: /tables/PatientAssessment

GET Request: returns LIST of all PatientAssessment Table entries made by patients within a certain Cluster Location

Returned fields: index, questionnaireStatus, start, end, assess_patientID, assess_questionnaireID
Body parameters: clusterID - cluster in which the patient's householdID is registered under (household's parentLocID)
Key: clusterID
Example: 
{
    "clusterID":"33"
}

POST Request
Example:
{
	"data": [{
		"assess_patientID":"31",
		"assess_questionnaireID":"3",
		"questionnaireStatus":"COMPLETE",
		"start":"2020-02-21",
		"end":"2020-02-29"
	}]
}
"""
class PatientAssessmentTable(APIView):
    def get(self, request):
        location = request.GET.get("clusterID")
        # Exception of no data found
        data = PatientAssessment.objects.filter(assess_patientID__householdID__parentLocID = location)
        serializer = PatientAssessmentSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        # An array of PatientAssessment Table Entries
        results = []
        data = request.data
        for item in data['data']:
            patient = get_object_or_404(Patient, pk=item['assess_patientID'])
            questionnaire = get_object_or_404(Questionnaire, pk=item['assess_questionnaireID'])
            if item['last_answered_qn'] != -1:
                question = get_object_or_404(Questions, pk=item['last_answered_qn'])
            else:
                question = None

            person, created = PatientAssessment.objects.get_or_create(
                assess_patientID = patient, 
                assess_questionnaireID = questionnaire, 
                start = item['start'],
                defaults = {'questionnaireStatus': item['questionnaireStatus'], 'end': item['end'], 'last_answered_qn':question})
            
            if created == False:
                person.questionnaireStatus = item['questionnaireStatus']
                person.end = item['end']
                person.last_answered_qn = None
                person.save()
            results.append(person)   
        serializer = PatientAssessmentSerializer(results, many = True)
        return Response(serializer.data)

class QuestionResponseTable(APIView):
    def get(self, request):
        clusterID = request.GET.get("clusterID")
        data = QuestionResponse.objects.filter(patientID__householdID__parentLocID = clusterID)
        serializer = QuestionResponseSerializer(data, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        results = []
        responses = request.data
        for response in responses['data']: 
            patient = get_object_or_404(Patient, patientID=response['patientID'])
            question = get_object_or_404(Questions, pk=response['questionID'])
            answer = get_object_or_404(Answer, pk=response['answerID'])
            questionnaire = get_object_or_404(Questionnaire, pk=response['questionnaireID'])
            responseInstance, created = QuestionResponse.objects.get_or_create(
                                                patientID=patient, 
                                                questionID=question, 
                                                answerID=answer, 
                                                text=response['text'], 
                                                questionnaireID=questionnaire,
                                                date=response['date'])
            if created == False:
                print("already existed")
                responseInstance.save()

            results.append(QuestionResponse.objects.get(pk=responseInstance.index))
        serializer = QuestionResponseSerializer(results, many=True)
        return Response(serializer.data)

class HouseholeTable(APIView):
    def get(self, request):
        clusterID = request.GET.get("clusterID")
        data = HouseHold.objects.filter(parentLocID=clusterID)
        serializer = HouseholdSerializer(data, many=True)
        return Response(serializer.data)
# /tables/Household?clusterID=34

    def post(self, request):
        results = []
        responses = request.data
        for response in responses['data']:
            parentLocID = get_object_or_404(Location, locationID=response['parentLocID'])
            enumeratorID = get_object_or_404(Enumerator, enumeratorID=response['enumeratorID'])
            responseInstance, created = HouseHold.objects.get_or_create(
                householdID=response['householdID'],
                parentLocID=parentLocID,
                enumeratorID=enumeratorID,
                date=response['date'],
                village_street_name=response['village_street_name'],
                gps_latitude=response['gps_latitude'],
                gps_longitude=response['gps_longitude'],
                availability=response['availability'],
                reason_refusal=response['reason_refusal'],
                visit_num=response['visit_num'],
                key_informer=response['key_informer'],
                tel1_num=response['tel1_num'],
                tel1_owner=response['tel1_owner'],
                tel2_num=response['tel2_num'],
                tel2_owner=response['tel2_owner'],
                consent=response['consent'],
                a2q1=response['a2q1'],
                a2q2=response['a2q2'],
                a2q3=response['a2q3'],
                a2q4=response['a2q4'],
                a2q5=response['a2q5'],
                a2q6=response['a2q6'],
                a2q7=response['a2q7'],
                a2q8=response['a2q8'],
                a2q9=response['a2q9'],
                a2q10=response['a2q10'],
                a2q11=response['a2q11'],
                a2q12=response['a2q12'],
                a2q13=response['a2q13']
            )
            if created == False:
                responseInstance.save()
            results.append(HouseHold.objects.get(householdID=responseInstance.householdID))
        serializer = HouseholdSerializer(results, many=True)
        return Response(serializer.data)
            
# https://books.agiliq.com/projects/django-api-polls-tutorial/en/latest/access-control.html#creating-a-user
# For developer use only -> should not be able to create new users from the website, only admin allowed to add new users
class UserCreate(generics.CreateAPIView):
    # Override the global setting: isAuthenticated
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer
    # {
    # "username": "nate.silver",
    # "email": "nate.silver@example.com",
    # "password": "FiveThirtyEight"
    # }   


# API Version of Login
class LoginView(APIView):
    permission_classes = ()
    def post(self, request,):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong credentials"}, status=status.HTTP_400_BAD_REQUEST)
