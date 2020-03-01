from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from Locations.models import Location
from Questions.models import *


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = 'locationID', 'locationName', 'parentLocID'

class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = 'questionnaireID', 'questionnaireName', 'questionnaireVersion'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = 'questionID', 'questionString', 'answerMin', 'answerMax', 'questionInstruction', 'questionMedia', 'questionTypeID', 'questionnaireID'

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = 'answerID', 'answerString', 'questionnaireID'

class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta: 
        model = QuestionAnswer
        fields = 'questionID', 'answerID', 'questionnaireID'

class LogicSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Logic
        fields = 'seq_num', 'logic_questionID', 'rel_ans_ID', 'next_qID', 'rel_type', 'rel_ID', 'questionnaireID'
    
class QRelSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionRelation
        fields = 'question_rel_questionID', 'questionnaireID', 'rel_ID', 'rel_ans_ID', 'rel_qID'

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = 'patientID', 'studyID', 'date_of_birth', 'prefix', 'firstName', 'middleName', 'lastName', 'suffix', 'com_name', 'gender', 'householdID', 'dur_hh', 'exam_status', 'notes', 'lvl_edu', 'work_status', 'marital_status', 
        'motherFirstName', 'motherLastName', 'tel1_num', 'tel1_owner', 'tel1_owner_rel', 'tel2_num', 'tel2_owner', 'tel2_owner_rel', 'enumeratorID', 'nationalID', 'deceased', 'deceased_date', 'responder', 'proxy_name', 'proxy_rel'

class PatientAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientAssessment
        fields = 'index', 'assess_patientID', 'assess_questionnaireID', 'questionnaireStatus', 'start', 'end'

class QuestionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionResponse
        fields = 'patientID', 'questionID', 'answerID', 'text', 'questionnaireID', 'date'


# https://books.agiliq.com/projects/django-api-polls-tutorial/en/latest/access-control.html#creating-a-user
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        # Ensure that we do not get back the password in Response
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user