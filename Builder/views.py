from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from collections import OrderedDict
from django.template import RequestContext
from django.template import loader
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from API.serializers import *
from Questions.models import *
from .forms import *

@login_required
def questionnaires(request):
    questionnaires = Questionnaire.objects.all() 
    template = loader.get_template('questionnaires.html')
    data = []
    for questionnaire in questionnaires:
            questionList = []
            question = Questions.objects.filter(questionnaireID = questionnaire.questionnaireID)
            serializers = QuestionSerializer(question, many=True)
            for stuff in serializers.data:
                # https://stackoverflow.com/questions/10058140/accessing-items-in-an-collections-ordereddict-by-index
                questionList.append(list(stuff.items()))
            data.append({
                'questionnaireID': questionnaire.questionnaireID, 
                'questionnaireName': questionnaire.questionnaireName,
                'question': questionList,
                })               
    context = {
        'data': data,
    }
    return HttpResponse(template.render(context, request))

@login_required
def newQuestionnaire(request):
    if request.method == 'POST':
        form = questionnaireForm(request.POST)
        if form.is_valid():
            new_qnn = form.save()
            return redirect('question/%s/' % new_qnn.questionnaireID)
    
    form = questionnaireForm()
    return render(request, 'new_questionnaire.html', {'form': form} )


@login_required
def addQuestions(request, questionnaire_id):
    rangeArray = []
    if request.method == 'POST':
        form = questionForm(request.POST)
        if form.is_valid():
            
            questionString = form.cleaned_data['question']
            questionTypeID = QuestionType.objects.get(questionTypeID=form.cleaned_data['questionTypeID'])
            answerMin = form.cleaned_data['answerMin']
            answerMax = form.cleaned_data['answerMax']
            questionInstruction = form.cleaned_data['questionInstruction']

            question = Questions.objects.create(questionString=questionString, 
                                questionTypeID=questionTypeID, 
                                answerMin=answerMin,
                                answerMax=answerMax,
                                questionInstruction=questionInstruction,
                                questionnaireID = Questionnaire.objects.get(pk=questionnaire_id))
            
            if questionTypeID.questionType == 'Text':
                return redirect('/questionnaires/create/question/%s/' % questionnaire_id)
            else:
                return redirect('answers/%s/' % question.pk)

    questionnaire = get_object_or_404(Questionnaire, pk=questionnaire_id)
    questions = Questions.objects.filter(questionnaireID=questionnaire_id).values('questionID','questionString')
    answers = QuestionAnswer.objects.filter(questionnaireID=questionnaire_id).select_related('answerID')
    answer_array = []
    for question in questions:
        answerString = QuestionAnswer.objects.select_related().filter(questionnaireID=questionnaire_id, questionID = question['questionID'])
        temp_array = []
        for answers in answerString:
            temp_array.append(answers.answerID.answerString)
        answer_array.append(temp_array)
    form = questionForm()
    context= {
        'questionnaire':questionnaire,
        'questions': questions,
        'answers': answer_array,
        'form':form,
        } 
    return render(request, 'question_qnn.html', context)



@login_required
def addAnswers(request, questionnaire_id, question_id):
    question = get_object_or_404(Questions, pk=question_id)
    questionnaire = get_object_or_404(Questionnaire, pk=questionnaire_id)
    
    if request.method == 'POST':
        form = answerForm(request.POST)
        if form.is_valid():
            answerString = form.cleaned_data['customAnswer']
            answer, created = Answer.objects.get_or_create(answerString = answerString,
                                            questionnaireID = questionnaire)
            QuestionAnswer.objects.get_or_create(questionID=question, answerID=answer, questionnaireID=questionnaire)       
        else:
            print(form._errors)
            
    form = answerForm()
    answers = QuestionAnswer.objects.filter(questionnaireID=questionnaire_id, questionID=question_id).select_related()
    context= {
        'questionnaire_id': questionnaire_id,
        'answers': answers,
        'form': form,
    }
    return render(request, 'ans_qnn.html', context)


@login_required
def addLogic(request, questionnaire_id):
    formset = qrelFormset(request.GET or None, form_kwargs={'questionnaire_id': questionnaire_id})
    questionnaire = Questionnaire.objects.get(pk=questionnaire_id)

    try:
        next_seq_num = Logic.objects.filter(questionnaireID = questionnaire_id).latest('seq_num').seq_num + 1
    except:
        next_seq_num = 1

    try:
        next_rel_id = Logic.objects.latest('rel_ID').rel_ID + 1
    except:
        next_rel_id = 1

    if request.method == 'POST':
        lForm = logicForm(request.POST, questionnaire_id= questionnaire_id)
        formset = qrelFormset(request.POST, form_kwargs={'questionnaire_id': questionnaire_id})
        
        if lForm.is_valid():
            currentQForm = lForm.cleaned_data['currentQ']
            currentQ = get_object_or_404(Questions, pk=currentQForm)
            nextQForm = lForm.cleaned_data['nextQ']
            nextQ = get_object_or_404(Questions, pk=nextQForm)
            relationship = lForm.cleaned_data['relation']
            if(relationship == "INSEQ"):
                Logic.objects.get_or_create(seq_num=next_seq_num, 
                                    logic_questionID=currentQ, 
                                    rel_ans_ID = None, 
                                    next_qID=nextQ,
                                    rel_type="INSEQ",
                                    rel_ID = None,
                                    questionnaireID = questionnaire)
            elif(relationship == "NEXT"):
                answerNextform = lForm.cleaned_data['answerNext']
                answerNext = get_object_or_404(Answer, pk=answerNextform)
                Logic.objects.get_or_create(
                                    seq_num=next_seq_num, 
                                    logic_questionID=currentQ, 
                                    rel_ans_ID = answerNext, 
                                    next_qID=nextQ,
                                    rel_type="NEXT",
                                    rel_ID = None,
                                    questionnaireID = questionnaire)
            else:
                if formset.is_valid():
                    logic, create = Logic.objects.get_or_create(
                                        seq_num=next_seq_num, 
                                        logic_questionID=currentQ, 
                                        rel_ans_ID = None, 
                                        next_qID=nextQ,
                                        rel_type=relationship,
                                        rel_ID = next_rel_id,
                                        questionnaireID=questionnaire)
                    for form in formset:
                        conditionalQuestionForm = form.cleaned_data.get('conditionalQuestion')
                        conditionalAnswerForm = form.cleaned_data.get('conditionalAnswer')
                        conditonalQuestion = get_object_or_404(Questions, pk=conditionalQuestionForm)
                        conditionalAnswer = get_object_or_404(Answer, pk=conditionalAnswerForm)
                        QuestionRelation.objects.get_or_create(rel_ID=logic, 
                                                                question_rel_questionID=currentQ,
                                                                rel_qID=conditonalQuestion,
                                                                rel_ans_ID=conditionalAnswer,
                                                                questionnaireID=questionnaire)
    
    questions = Questions.objects.filter(questionnaireID = questionnaire_id)
    answers = Answer.objects.filter(questionnaireID = questionnaire_id)
    # logForm = logicForm(questionnaire_id)
    lForm = logicForm(questionnaire_id= questionnaire_id)
    logic = Logic.objects.filter(questionnaireID = questionnaire_id).order_by('seq_num').select_related()
    context= {
        'questionnaire_id': questionnaire_id,
        'logicForm': lForm,
        'formset': formset,
        'logic': logic,
    }

    return render(request, 'logic.html', context)


@login_required
def ajaxAnswer(request):
    questionnaire_id = request.GET.get('questionnaire_id')
    question_id = request.GET.get('question_id')
    questionAnswers = QuestionAnswer.objects.filter(questionID = question_id, questionnaireID = questionnaire_id).select_related()
    answers = []
    for question in questionAnswers:
        answers.append(str(question.answerID.answerID))
    return JsonResponse({'answers': answers})


