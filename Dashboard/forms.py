from django import forms
from Questions.models import PatientAssessment
from Locations.models import *

class dashboardForm(forms.Form):
    country = forms.ChoiceField(label='Country', widget=forms.Select)
    region = forms.ChoiceField(label='Region', widget=forms.Select)
    cluster = forms.ChoiceField(label='Cluster', widget=forms.Select)

    def __init__(self, *args, **kwargs):
        super(dashboardForm, self).__init__(*args, **kwargs)
        emptyChoiceList = [('null', '----------')]
        print(Location.objects.all().values())
        countryList = [(country.locationID, country.locationName) for country in Location.objects.filter(locationID = '-1')]
        choices = emptyChoiceList + countryList
        self.fields['country'].choices = choices