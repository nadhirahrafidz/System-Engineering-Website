from django import forms

class enumeratorTokenForm(forms.Form):
    username = forms.CharField( label='Username',
                                max_length=150, 
                                help_text='150 characters or fewer. Letters, digits and @/./+/-/_ only',
                                error_messages={'required': 'Please enter a username'})
    email = forms.EmailField(label='E-mail')
    password = forms.PasswordInput(label='Password')