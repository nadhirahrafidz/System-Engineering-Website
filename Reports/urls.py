from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.chooseLocation, name='report_location'),
    path('qnn/<str:clusterID>/', views.chooseQuestionnaire, name='report_qnn'),
    path('qnn/<str:clusterID>/<str:questionnaireID>/', views.reportQnn, name='report')
]