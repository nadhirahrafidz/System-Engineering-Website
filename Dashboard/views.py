from django.shortcuts import render
from django.template import loader
from .forms import *

def DashboardView(request):
    form = dashboardForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard.html', context)

# Create your views here.
