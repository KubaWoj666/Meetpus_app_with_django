from django import forms

from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from.models import Meetup, Location, Company


class MeetupForm(forms.ModelForm):
    class Meta:
        model = Meetup
        exclude = ["created", "slug", "organizer", "participants"]
        widgets = {
            "date": forms.DateInput(attrs={'type': 'date'}),
            
        }

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = "__all__"

                 

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email']


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ["creator"]

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]