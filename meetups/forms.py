from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

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
        labels = {
            "name" : "Company Name"
        }



class ParticipantForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]