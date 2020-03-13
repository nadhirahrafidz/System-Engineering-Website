from django import forms
from . import models
from functools import partial


class enumeratorTokenForm(forms.Form):
    username = forms.CharField( label='Username',
                                max_length=150, 
                                help_text='150 characters or fewer. Letters, digits and @/./+/-/_ only',
                                error_messages={'required': 'Please enter a username'})
    email = forms.EmailField(label='E-mail')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class enumeratorTableForm(forms.Form):
        prefix = forms.ChoiceField(label='Prefix', choices=[('MR', 'Mr'),('MRS', 'Mrs'),('MISS', 'Miss'),('MS', 'Ms'),('DR', 'Dr')])
        firstName = forms.CharField(label='First Name')
        lastName = forms.CharField(label='Last Name')
        suffix = forms.CharField(label='Suffix', required=False)
        organization = forms.CharField(label='Organization', required=False)
        date_of_birth = forms.CharField(label='Date of Birth', help_text='Input format is DD/MM/YY')
        active_flag = forms.ChoiceField(label='Activity Status', choices=[('1', 'Active'), ('2', 'Inactive')], help_text='Set "Active" if enumerator is currently active on the field or "Inactive" if the enumerator is not currently active on the field')