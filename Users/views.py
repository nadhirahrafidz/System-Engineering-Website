from django.shortcuts import render, redirect
from django.db import IntegrityError
from Users.models import *
from Users.forms import *
import requests 
import json

# Create your views here.
def getToken(request):
    form = enumeratorTokenForm()
    if request.method == 'POST':
        form = enumeratorTokenForm(request.POST)
        if form.is_valid():
            data ={
                "username": form.cleaned_data['username'],
                "email": form.cleaned_data['email'],
                "password": form.cleaned_data['password'],
            }
            headers = {
                'Content-type': 'application/json',
                }
            # Hard coded URL
            r = requests.post('http://127.0.0.1:8000/users/', data=json.dumps(data), headers=headers)
            if r.status_code == 201 or r.status_code == 200:
                data ={
                    "username": form.cleaned_data['username'],
                    "password": form.cleaned_data['password'],
                }
                token_request = requests.post('http://127.0.0.1:8000/tables/login/', data=json.dumps(data), headers=headers)
                token_dict = token_request.text
                token = json.loads(token_dict)['token']
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                return redirect('add/%s/%s/%s/' % (token, username, email))
            # ERROR HANDLING IF FORM IS NOT VALID
    context ={
        "form": form,
    }
    return render(request, 'enumerator_token.html', context)

def addEnumerator(request, token, username, email):
    if request.method == 'POST':
        print("posting")
        form = enumeratorTableForm(request.POST)
        if form.is_valid():
            print("valid")
            try:
                enumerator, created = Enumerator.objects.get_or_create(
                    enumeratorID=token,
                    prefix=form.cleaned_data['prefix'],
                    firstName=form.cleaned_data['firstName'],
                    lastName=form.cleaned_data['lastName'],
                    suffix=form.cleaned_data['suffix'],
                    organization=form.cleaned_data['organization'],
                    date_of_birth=form.cleaned_data['date_of_birth'],
                    active_flag= form.cleaned_data['active_flag'],             
                    username= username,
                    email = email
                )
                
            except IntegrityError as e:
                print("Integrity Error")
                return redirect('status/%i' % 0)

            print("about to render")
            return redirect('/enumerators/status/%i' % 1)

    print("normal rendering")      
    form = enumeratorTableForm()
    context = {
        "form" : form
    }
    return render(request, 'enumerator_table.html', context)

def response_message(request, status):
    if status == 1:
        context = {
            "message": "Successfully Registered Enumerator"
        }
    else:
        context = {
            "message": "Integrity Error: Enumerator Already Exists"
        }
    return render(request, 'response_message.html', context)