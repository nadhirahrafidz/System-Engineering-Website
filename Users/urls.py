from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.getToken, name='getToken'),
    path('add/<str:token>/<str:username>/<str:email>/', views.addEnumerator, name='addEnum'),
    path('status/<int:status>', views.response_message, name='responseMessage'),
]