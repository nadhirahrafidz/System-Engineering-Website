from django.conf.urls import url
# from .views import questionnaires_view as qv
from django.urls import path
from . import views

urlpatterns = [
    # url(r'^$', qv.as_view(extra_context = {'text':qv.questionList}), name='questionnaires'),
    path('', views.questionnaires, name='questionnaires'),
    path('create/', views.newQuestionnaire, name='newQuestionnaire'),
    path('create/question/<int:questionnaire_id>/', views.addQuestions, name='addQuestions'),
    path('create/question/<int:questionnaire_id>/answers/<int:question_id>/', views.addAnswers, name='addAnswers'),
    path('create/question/<int:questionnaire_id>/logic', views.addLogic, name='addLogic'),
    path('ajax/', views.ajaxAnswer, name='ajax_answer'),
    path('setactive/', views.setActiveQnn, name='setActiveQnn'),
]