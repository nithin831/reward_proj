# rewards/forms.py
from django import forms
from .models import App, Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class AdminAppForm(forms.ModelForm):
    class Meta:
        model = App
        fields = ['name', 'download_link', 'points']

class UserSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['screenshot']
