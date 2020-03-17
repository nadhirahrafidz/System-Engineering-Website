from django import forms
from Questions.models import *
from django.forms import formset_factory

"""
    Holds all the forms used in the website's Questionnaire Builder Feature. 
    List of questionnaires:
    1. Create a new questionnaire form (class questionnaireForm)
    2. Set active questionnaires (class activeQnnForm)
    3. Create new questions form (class questionForm)
    4. Create new answers form for a questionnaire (class answerForm)
    5. Set Logic for Questionnaire (class logicForm)
    6. Set 'OR' and 'AND' logic for Questionnaire Logic [to be inserted in questionrelation Table] (class qrelForm)
"""
class questionnaireForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = ('questionnaireName', 'questionnaireVersion', 'questionnaireType')
        labels = {
            'questionnaireName': ('Questionnaire Name:'),
            'questionnaireVersion': ('Questionnaire Version:'),
            'questionnaireType': ('Questionnaire Category:'),
        }

class activeQnnForm(forms.Form):
    householdQnn = forms.ChoiceField(label='Household Questionnaire')
    patientQnn = forms.ChoiceField(label='Patient Registration Questionnaire')
    generalQnn = forms.ChoiceField(label='General Questionnaire')
    mobilityQnn = forms.ChoiceField(label='Mobility Questionnaire')
    visionQnn = forms.ChoiceField(label='Vision Questionnaire')
    hearingQnn = forms.ChoiceField(label='Hearing Questionnaire')

    # Prepopulating the form's ChoiceFields with questionnaires from the server database
    def __init__(self, *args,**kwargs):
        super(activeQnnForm, self).__init__(*args, **kwargs)
        householdList = [(qnn.questionnaireID, qnn.questionnaireName) for qnn in Questionnaire.objects.filter(questionnaireType = "HOUSEHOLD")]
        patientList = [(qnn.questionnaireID, qnn.questionnaireName) for qnn in Questionnaire.objects.filter(questionnaireType = "PATIENT_INFO")]
        generalList = [(qnn.questionnaireID, qnn.questionnaireName) for qnn in Questionnaire.objects.filter(questionnaireType = "GENERAL")]
        mobilityList = [(qnn.questionnaireID, qnn.questionnaireName) for qnn in Questionnaire.objects.filter(questionnaireType = "MOBILITY")]
        visionList = [(qnn.questionnaireID, qnn.questionnaireName) for qnn in Questionnaire.objects.filter(questionnaireType = "VISION")]
        hearingList = [(qnn.questionnaireID, qnn.questionnaireName) for qnn in Questionnaire.objects.filter(questionnaireType = "HEARING")]
        self.fields['householdQnn'].choices = householdList
        self.fields['patientQnn'].choices = patientList
        self.fields['generalQnn'].choices = generalList
        self.fields['mobilityQnn'].choices = mobilityList
        self.fields['visionQnn'].choices = visionList
        self.fields['hearingQnn'].choices = hearingList

class questionForm(forms.Form):
    question = forms.CharField(label='Question', widget=forms.Textarea(attrs={"rows":3, "cols":20}), max_length=300)
    CHOICES = [('1', 'Single Answer'), ('2', 'Multiple Answers'), ('3', 'Text Answer')]
    questionTypeID = forms.ChoiceField(label='Question Type', widget=forms.Select, choices=CHOICES)
    answerMin = forms.IntegerField(label='Minimum Answer', initial=1)
    answerMax = forms.IntegerField(label='Maximum Answer', initial=1)
    questionInstruction = forms.CharField(label='Question Instructions', widget=forms.Textarea(attrs={"rows":4, "cols":20}), max_length=300, required=False)
   
class answerForm(forms.Form):
    customAnswer = forms.CharField(label='Custom Answer', max_length=300)


class logicForm(forms.Form):
    currentQ = forms.ChoiceField(label='Current Question', widget=forms.Select)
    nextQ = forms.ChoiceField(label='Next Question', widget=forms.Select)
    RELCHOICES = [('INSEQ','In Sequence'), ('NEXT', 'IF Condition') , ('AND','AND Condition'), ('OR', 'OR Condition')]
    relation = forms.ChoiceField(label='Relationship', widget=forms.Select, choices=RELCHOICES)
    answerNext = forms.ChoiceField(label='Conditional Answer', widget=forms.Select)

    # Pre-populating the ChoiceFields with existing questions and answers for a specific questionnaire
    def __init__(self, *args,**kwargs):
        self.questionnaire_id = kwargs.pop("questionnaire_id")
        super(logicForm, self).__init__(*args, **kwargs)
        emptyChoiceList = [('null', '----------')]
        questionList = [(question.questionID, question.questionString) for question in Questions.objects.filter(questionnaireID= self.questionnaire_id)]
        answerList = [(answer.answerID, answer.answerString) for answer in Answer.objects.filter(questionnaireID= self.questionnaire_id)]
        nextQuestionList = emptyChoiceList + questionList
        self.fields['currentQ'].choices = questionList
        self.fields['nextQ'].choices = nextQuestionList
        self.fields['answerNext'].choices = answerList

class qrelForm(forms.Form):
    conditionalQuestion = forms.ChoiceField(label='Conditional Question', 
                                            widget=forms.Select(attrs={
                                                'class': 'form-control',
                                            }))
    conditionalAnswer = forms.ChoiceField(label='ConditionalAnswer', 
                                            widget=forms.Select(attrs={
                                                'class': 'form-control',
                                            }))
    
    def __init__(self, questionnaire_id, *args, **kwargs):
        super(qrelForm, self).__init__(*args, **kwargs)
        questionList = [(question.questionID, question.questionString) for question in Questions.objects.filter(questionnaireID=questionnaire_id)]
        answerList = [(answer.answerID, answer.answerString) for answer in Answer.objects.filter(questionnaireID= questionnaire_id)]
        self.fields['conditionalQuestion'].choices = questionList
        self.fields['conditionalAnswer'].choices = answerList

qrelFormset = formset_factory(qrelForm, extra=1)