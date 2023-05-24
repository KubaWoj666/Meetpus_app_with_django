from django.core.exceptions import ValidationError
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify

from django.contrib.auth.models import User, Group
from.models import Meetup, Location
from .forms import UserCreationForm, MeetupForm, LocationForm
from django.contrib.auth.forms import AuthenticationForm

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

@login_required(login_url="login")
@permission_required("meetups.add_meetup", login_url='/login', raise_exception=True)
def create_meetup_view(request):
    locations = Location.objects.all()
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
            "form":form,
            "locations":locations,
        }
    except ValidationError as err:
        form = MeetupForm
        error_message = ", ".join(err)

        context = {
            "form" : form,
            "locations":locations,
            "error_message": error_message
        }
        return render(request, "meetups/create_meetup.html", context)


    return render(request, "meetups/create_meetup.html", context)

@login_required(login_url="login")
@permission_required('meetups.add_location', login_url='/login', raise_exception=True)
def add_new_location_view(request):
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'newLocation'})
    else:
        form = LocationForm()

    context = {
        "form": form
    }

    return render(request, "meetups/create_location.html", context )
        


def sign_up_user_view(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("default_or_creator", pk=user.id)
    else:
        form = UserCreationForm()
        
    context = {
        "form": form,
    }
    
    return render(request, "meetups/sign_up_user.html", context)


def default_or_creator_view(request, pk):
    if request.method == "POST":
        user = User.objects.get(id=pk)
        group = request.POST.get("group")
        print(group)
        if group:
            group_obj = Group.objects.get(name=group)
            user.groups.add(group_obj)
            user.save()
            return redirect("home")
    
    return render(request, "meetups/default_or_creator.html", {} )

def login_view(request):
    error_message = None
    form = AuthenticationForm

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
        else:
            error_message = 'Invalid credentials'

    context = {
        'form':form,
        'error_message': error_message,
    }
    
    return render(request, "meetups/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("home")


def get_last_location_view(request):
    
    last_loc = Location.objects.last()
    html = "<label for='id_location'>Location:</label><select name='location' required id='id_location'><option value='%s' selected>%s</option></select>" %(last_loc.id,last_loc)
    return HttpResponse(html)