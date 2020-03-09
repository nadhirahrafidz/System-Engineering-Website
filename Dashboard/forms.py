from django import forms
from Questions.models import PatientAssessment
from Locations.models import *

class dashboardForm(forms.Form):
    country = forms.ChoiceField(label='Country', widget=forms.Select)
    region = forms.ChoiceField(label='Region', widget=forms.Select)
    cluster = forms.ChoiceField(label='Cluster', widget=forms.Select)

    def __init__(self, *args, **kwargs):
        super(dashboardForm, self).__init__(*args, **kwargs)
        emptyChoiceList = [('0', '----------')]
        countryList = [(country.locationID, country.locationName) for country in Location.objects.filter(parentLocID = -1)]
        allLocations = [(location.locationID, location.locationName) for location in Location.objects.all().exclude(pk = -1)]
        countryChoices = emptyChoiceList + countryList
        otherChoices = emptyChoiceList + allLocations
        self.fields['country'].choices = countryChoices
        self.fields['region'].choices = otherChoices
        self.fields['cluster'].choices = otherChoices