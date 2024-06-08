from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class loginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
          'placeholder':'Enter Password',
        'class': 'form-form-control pe-5 password-input'
    }))