from django.shortcuts import render
from .models import Location,HouseHold


def get_countries(request):
    countries = Location.objects.filter(parentLocID='-1')
    return render(request, 'reports.html', {'countries': countries})


def get_regions(request, id):
    regions = Location.objects.filter(parentLocID=id)
    return render(request, 'reports.html', {'regions': regions})


def get_clusters(request, id):
    print(id)
    clusters = Location.objects.filter(parentLocID=id)
    return render(request, 'reports.html', {'clusters': clusters})