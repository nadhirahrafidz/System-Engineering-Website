from django.conf.urls import url
from . import views as api_views
urlpatterns = [
    url(r'^Location', api_views.LocationTable.as_view(), name='LocationTableAPI'),
    url(r'^Questionnaire', api_views.QuestionnaireTable.as_view(), name='QuestionnaireTableAPI'),
    url(r'^Question', api_views.QuestionTable.as_view(), name='QuestionTableAPI'),
    url(r'^Answer', api_views.AnswerTable.as_view(), name='AnswerTableAPI'),
    url(r'^QA', api_views.QuestionAnswerTable.as_view(), name='QATableAPI'),
    url(r'^Logic', api_views.LogicTable.as_view(), name='LogicTableAPI'),
    url(r'^QRel', api_views.QRelTable.as_view(), name='QRelTableAPI'),
    url(r'^login', api_views.LoginView.as_view(), name='LoginAPI'),
    url(r'^Patients', api_views.PatientTable.as_view(), name='PatientAPI'),
    url(r'^PatientAssessment', api_views.PatientAssessmentTable.as_view(), name='PatientAPI'),
    url(r'^Response', api_views.QuestionResponseTable.as_view(), name='QuestionResponseAPI'),
    url(r'^Household', api_views.HouseholeTable.as_view(), name='HouseholdAPI'),
]