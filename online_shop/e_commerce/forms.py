from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from .models import Profile

from django.contrib.auth.models import User

class createUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']

class ProfileForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Profile
        fields = ('address', 'image')