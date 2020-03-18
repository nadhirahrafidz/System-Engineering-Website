from django.test import TestCase
from django.urls import reverse
from rest_framework.test import force_authenticate, APIRequestFactory, APITestCase
from rest_framework import status
from rest_framework.test import RequestsClient
import json
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from Patients.models import *
from Locations.models import *
from django.db import transaction
# Create your tests here.

class patientTest(APITestCase):

    def setUp(self):
        self.username = 'john_doe'
        self.password = 'foobar'
        with transaction.atomic():
            self.user = User.objects.create(username= self.username, password=self.password)
            data = {
                "username": self.username,
                "password": self.password
            }
            token = Token.objects.create(user = self.user)
            self.client = APIClient()
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    
    def test_registration(self):
        data = {
            "username": "test-user", 
            "email": "test@gmail.com", 
            "password": "something-strong"
        }
        c = RequestsClient()
        response = c.post("http://127.0.0.1:8000/users/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_registration_duplicate(self):
        data = {
            "username": "test-user", 
            "email": "test@gmail.com", 
            "password": "something-strong"
        }
        c = RequestsClient()
        response = c.post("http://127.0.0.1:8000/users/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        data_login = {
            "username": "test-user",
            "password": "something-strong"
        }
        c = RequestsClient()
        response = c.post("http://127.0.0.1:8000/login/", data_login)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_Location(self):
        Location.objects.create(
            locationID="1",
            locationName="Malaysia",
            parentLocID = None
        )
        response = self.client.get("http://127.0.0.1:8000/tables/Location")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
