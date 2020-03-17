from django.db import models
from datetime import date

from Patients.models import Patient


class Questionnaire(models.Model):
    BOOLEAN = (
        (1, 'True'),
        (0, 'False'),
    )
    CATEGORY = (
        ("MOBILITY", 'Mobility Questionnaire'),
        ("VISION", 'Vision Questionnaire'),
        ("HEARING", 'Hearing Questionnaire'),
        ("GENERAL", 'General Questionnaire'),
        ("HOUSEHOLD", 'Household Questionnaire'),
        ("PATIENT_INFO", 'Patient Registration Questionnaire'),
    )
    questionnaireID = models.AutoField(verbose_name='questionnaireID', primary_key=True)
    questionnaireName = models.CharField(verbose_name='questionnaireName', max_length=100)
    questionnaireVersion = models.CharField(verbose_name='questionnaireVersion', max_length=45)
    active_flag = models.IntegerField(verbose_name='active_flag', default=0, choices=BOOLEAN)
    questionnaireType = models.CharField(verbose_name='questionnaire_type', max_length=45, choices=CATEGORY)


class QuestionType(models.Model):
    QTYPE = (
        ('S', 'Single'),
        ('M', 'Multiple'),
        ('T', 'Text'),
    )
    questionTypeID = models.AutoField(verbose_name='questionTypeID', primary_key=True)
    questionType = models.CharField(verbose_name='questionType', max_length=10, choices=QTYPE)


class Questions(models.Model):
    questionID = models.AutoField(verbose_name='questionID', primary_key=True)
    questionString = models.CharField(verbose_name='questionString', max_length=300)
    questionTypeID = models.ForeignKey(QuestionType, verbose_name='questionTypeID', on_delete=models.CASCADE)
    answerMin = models.IntegerField(verbose_name='answer_min', default=1)
    answerMax = models.IntegerField(verbose_name='answer_max', default=1)
    questionInstruction = models.CharField(verbose_name='QuestionInstruction', max_length=300, blank=True)
    questionnaireID = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    questionMedia = models.CharField(max_length=45, blank=True)


class Answer(models.Model):
    answerID = models.AutoField(primary_key=True)
    answerString = models.CharField(max_length=300)
    questionnaireID = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)


class QuestionAnswer(models.Model):
    index = models.AutoField(primary_key=True)
    questionID = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answerID = models.ForeignKey(Answer, on_delete=models.CASCADE)
    questionnaireID = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)


class QuestionResponse(models.Model):
    index = models.AutoField(primary_key=True)
    patientID = models.ForeignKey(Patient, on_delete=models.CASCADE)
    questionID = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answerID = models.ForeignKey(Answer, on_delete=models.CASCADE, blank = True, null= True)
    text = models.CharField(verbose_name='text', blank=True, max_length=300)
    questionnaireID = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    date = models.CharField(max_length=35)

    # class Meta:
    #     db_table = 'Response'
    #     unique_together = ('patientID', 'questionID', 'answerID', 'questionnaireID', 'date')


class Logic(models.Model):
    REL_TYPE = (
        ('INSEQ', 'In Sequence'),
        ('NEXT', 'Next'),
        ('AND', 'And'),
        ('OR', 'Or'),
    )
    logic_id = models.AutoField(primary_key = True)
    seq_num = models.IntegerField(verbose_name='Sequence_Number')
    logic_questionID = models.ForeignKey(Questions, related_name='logic_questionID', on_delete=models.CASCADE)
    rel_ans_ID = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)
    next_qID = models.ForeignKey(Questions, related_name='next_qID', on_delete=models.CASCADE, null=True)
    rel_type = models.CharField(max_length=10, blank=True, choices=REL_TYPE)
    rel_ID = models.IntegerField(verbose_name='relationID', unique=True, null=True)
    questionnaireID = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)


class QuestionRelation(models.Model):
    index = models.AutoField(primary_key=True)
    rel_ID = models.ForeignKey(Logic, to_field='rel_ID', db_column='rel_ID', on_delete=models.CASCADE)
    question_rel_questionID = models.ForeignKey(Questions, related_name='question_rel_questionID', on_delete=models.CASCADE)
    rel_qID = models.ForeignKey(Questions, related_name='rel_qID', on_delete=models.CASCADE)
    rel_ans_ID = models.ForeignKey(Answer, on_delete=models.CASCADE)
    questionnaireID = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('rel_ID', 'question_rel_questionID', 'rel_qID', 'rel_ans_ID', 'questionnaireID')

# QuestionnaireStatus -> "COMPLETE", "INCOMPLETE" 
class PatientAssessment(models.Model):
    index = models.AutoField(primary_key=True)
    assess_patientID = models.ForeignKey(Patient, on_delete=models.CASCADE)
    assess_questionnaireID = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    questionnaireStatus = models.CharField(max_length=35)
    start = models.CharField(max_length=35, blank=True)
    end = models.CharField(max_length=35, blank=True)
    last_answered_qn = models.ForeignKey(Questions, to_field='questionID', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('assess_patientID', 'assess_questionnaireID', 'start')

