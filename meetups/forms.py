from django.forms import ModelForm, DateInput, TextInput

from.models import Meetup, Location, User, ProUser


class MeetupForm(ModelForm):
    class Meta:
        model = Meetup
        exclude = ["created", "slug" ]
        widgets = {
            "date": DateInput(attrs={'type': 'date'}),
            
        }

class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = "__all__"

        
                    

class UserCreationForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password", ]