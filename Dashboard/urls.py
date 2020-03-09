from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView, name='dashboard'),
    path('ajax/', views.ajaxLocation, name='ajaxLocation'),
    path('ajax/patient', views.ajaxIncompletePatients, name='ajaxPatient'),
    path('data/', views.ajaxData, name='ajaxData'),
]