from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauth.models import User
class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":'Username'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"placeholder":'Email'}))
    phone =forms.CharField(widget=forms.TextInput(attrs={"placeholder":'Phone number'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":'confirm Password'}))
    class Meta:
        model = User
        fields = ['username', 'email','phone']
