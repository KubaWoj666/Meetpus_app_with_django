from django import forms

from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from.models import Meetup, Location


class MeetupForm(forms.ModelForm):
    class Meta:
        model = Meetup
        exclude = ["created", "slug" ]
        widgets = {
            "date": forms.DateInput(attrs={'type': 'date'}),
            
        }

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = "__all__"

        
                    

# class UserCreationForm(forms.ModelForm):
#     group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)

#     class Meta:
#         model = User
#         fields = ["username",  "email", "password1", "password2", "group"]

class UserCreationForm(UserCreationForm):
    # group = forms.ModelChoiceField(queryset=Group.objects.all(),
    #                                required=True)
    
    class Meta:
        model = User
        fields = ['username','email']
# class LoginForm(AuthenticationForm):
#     class Meta:
#         model = User
#         fields = ["username", "password"]