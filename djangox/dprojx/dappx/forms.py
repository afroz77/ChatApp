from django import forms
from .models import UserProfileInfo
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):     
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(widget=forms.EmailInput())

    class Meta():
        model = User
        fields = ('username', 'password', 'email')


class UserProfileInfoForm(forms.ModelForm):

     class Meta():
         model = UserProfileInfo
         fields = ('portfolio_site','profile_pic')


class SignupForm(forms.ModelForm):
    email = forms.EmailField(max_length=100)
    class Meta:
        model = User
        fields = ('username', 'email')

