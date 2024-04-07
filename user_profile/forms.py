from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from user_profile.models import Credits


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class CreditsForm(forms.ModelForm):
    class Meta:
        model = Credits
        fields = ["credit"]
