from django.db import models

from Questions.models import Questions, Questionnaire


class Diagnosis(models.Model):
    index = models.AutoField(primary_key=True)
    questionDiagnosisID = models.ForeignKey(Questions, on_delete=models.CASCADE)
    questionnaireID = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('questionDiagnosisID', 'questionnaireID')


class Services(models.Model):
    index = models.AutoField(primary_key=True)
    questionServicesID = models.ForeignKey(Questions, on_delete=models.CASCADE)
    questionnaireID = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('questionServicesID', 'questionnaireID')


class AssistiveTechnology(models.Model):
    index = models.AutoField(primary_key=True)
    questionTechnologyID = models.ForeignKey(Questions, on_delete=models.CASCADE)
    questionnaireID = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('questionTechnologyID', 'questionnaireID')


class Cause(models.Model):
    index = models.AutoField(primary_key=True)
    questionCauseID = models.ForeignKey(Questions, on_delete=models.CASCADE)
    questionnaireID = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('questionCauseID', 'questionnaireID')
