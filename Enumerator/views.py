from django.shortcuts import render
from Users.models import *
from Enumerator.forms import *

# Create your views here.

def getToken(request):
    form = enumeratorTokenForm()
    # if request.method == 'POST':
    #     form = enumeratorTokenForm(request.POST)
    #     if form.is_valid():
    #         r = requests.post('/users/', params=request.POST)
    return render(request, 'enumerator_token.html')