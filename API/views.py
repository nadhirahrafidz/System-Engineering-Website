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


class LocationTable(APIView):
    def get(self, request):
        data = Location.objects.all()
        serializer = LocationSerializer(data, many=True)
        return Response(serializer.data)

class QuestionnaireTable(APIView):
    def get(self, request):
        data = Questionnaire.objects.all()
        serializer = QuestionnaireSerializer(data, many=True)
        return Response(serializer.data)

# Only retrieves questions for active questionnaires
class QuestionTable(APIView):
    def get(self, request):
        # Exception of no data found
        data = Questions.objects.filter(questionnaireID__active_flag=1)
        serializer = QuestionSerializer(data, many=True)
        return Response(serializer.data)

# Only retrieves answers for active questionnaires
class AnswerTable(APIView):
    def get(self, request):
        # Exception of no data found
        data = Answer.objects.filter(questionnaireID__active_flag=1)
        serializer = AnswerSerializer(data, many=True)
        return Response(serializer.data)

class QuestionAnswerTable(APIView):
    def get(self, request):
        # Exception of no data found
        data = QuestionAnswer.objects.filter(questionnaireID__active_flag=1)
        serializer = QuestionAnswerSerializer(data, many=True)
        return Response(serializer.data)

class LogicTable(APIView):
    def get(self, request):
        # Exception of no data found
        data = Logic.objects.filter(questionnaireID__active_flag=1)
        serializer = LogicSerializer(data, many=True)
        return Response(serializer.data)

class QRelTable(APIView):
    def get(self, request):
        # Exception of no data found
        data = QuestionRelation.objects.filter(questionnaireID__active_flag=1)
        serializer = QRelSerializer(data, many=True)
        return Response(serializer.data)

class PatientTable(APIView):
    def get(self, request):
        location = request.GET.get("clusterID")
        # Exception of no data found
        data = Patient.objects.filter(householdID__parentLocID = location)
        serializer = PatientSerializer(data, many=True)
        return Response(serializer.data)
        # {
	    #     "clusterID":"33"
        # }

class PatientAssessmentTable(APIView):
    def get(self, request):
        location = request.data.get("clusterID")
        # Exception of no data found
        data = PatientAssessment.objects.filter(assess_patientID__householdID__parentLocID = location)
        serializer = PatientAssessmentSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        # An array of PatientAssessment Table Entries
        results = []
        data = request.data.get("data")
        for item in data:
            patient = get_object_or_404(Patient, pk=item['assess_patientID'])
            questionnaire = get_object_or_404(Questionnaire, pk=item['assess_questionnaireID'])
            person, created = PatientAssessment.objects.get_or_create(
                assess_patientID = patient, 
                assess_questionnaireID = questionnaire, 
                start = item['start'],
                defaults = {'questionnaireStatus': item['questionnaireStatus'], 'end': item['end']})
            
            if created == False:
                person.questionnaireStatus = item['questionnaireStatus']
                person.end = item['end']
                person.save()
            results.append(person)   
        serializer = PatientAssessmentSerializer(results, many = True)
        return Response(serializer.data)

class QuestionResponseTable(APIView):
    def get(self, request):
        return Response("GET")
    
    def post(self, request):
        # results = []
        # body_unicode = request.data.get("data")
        # string_resp = [json.dumps(i) for i in body_unicode if i]
        # responses = [json.loads(i) for i in string_resp if i]
        # # responses = json.loads(body_unicode)
        # # responses = request.data.get("data")
        results = []
        responses = request.data
        for response in responses: 
            #print("response: " + response)
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
                responseInstance.save()

            results.append(QuestionResponse.objects.get(pk=responseInstance.index))
        serializer = QuestionResponseSerializer(results, many=True)
        return Response({"data": serializer.data})

class HouseholeTable(APIView):
    def get(self, request):
        clusterID = request.GET.get("clusterID")
        data = HouseHold.objects.filter(parentLocID=clusterID)
        serializer = HouseholdSerializer(data, many=True)
        return Response(serializer.data)
    def post(self, request):
        results = []
        responses = request.data
        for response in responses:
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
            print("success!")
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong credentials"}, status=status.HTTP_400_BAD_REQUEST)
