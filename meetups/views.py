from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.utils.text import slugify
from django.core.exceptions import ValidationError

from.models import Meetup, User, ProUser
from .forms import UserCreationForm, MeetupForm, LocationForm


def home_view(request):
    meetups = Meetup.objects.all()
    count_meetups = meetups.count()
    latest_meetups = meetups.order_by("-created")[:3]
    end_soon_meetups = meetups.order_by("date")[:3] 


    context = {
        "latest_meetups": latest_meetups,
        "end_soon_meetups": end_soon_meetups,
        "count_meetups": count_meetups,
    }

    return render(request, "meetups/home.html", context)


def detail_view(request, slug):
    try:
        meetup = Meetup.objects.get(slug=slug)

        context = {
            "meetup":meetup,
            "meetup_exist":True
        }
        return render(request, "meetups/detail.html" ,context)
    
    except Exception as exc:

        context = {
            "meetup_exist":False
        }
        return render(request, "meetups/detail.html" ,context)


def all_meetups_view(request):
    meetups = Meetup.objects.all()

    context = {
        "meetups": meetups,
    }

    return render(request, "meetups/all_meetups.html", context)


def search_meetups(request):
    q = request.GET.get("q") if request.GET.get("q") !=None else ""

    search_meetup = Meetup.objects.filter(Q(title__icontains=q) | 
                                          Q(location__country__icontains=q))

    context = {
        "search_meetup":search_meetup
    }

    return render(request, "meetups/search.html", context)


def create_meetup_view(request):
    error_message = None

    try:
        if request.method == "POST":
            form = MeetupForm(request.POST, request.FILES)
            if form.is_valid():
                meetup = form.save(commit=False)
                meetup.slug = slugify(meetup.title)
                meetup.save()
                return redirect("home")
        else:
            form = MeetupForm
                
        context = {
            "form":form
        }
    except ValidationError as err:
        form = MeetupForm
        error_message = ", ".join(err)
        print(error_message)

        context = {
            "form" : form,
            "error_message": error_message
        }
        return render(request, "meetups/create_meetup.html", context)


    return render(request, "meetups/create_meetup.html", context)


def add_new_location_view(request):
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect("create-meetup")
    else:
        form = LocationForm

    context = {
        "form": form
    }

    return render(request, "meetups/create_location.html", context )
        


def sign_up_view(request):
    
    return render(request, "meetups/sign_up.html", {})
    
