from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['email', 'message']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with provided email already exists")
        return self.cleaned_data

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['subject', 'message']
