from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify

from django.contrib.auth.models import User, Group
from.models import Meetup, Location
from .forms import UserCreationForm, MeetupForm, LocationForm, CompanyForm, ParticipantForm
from django.contrib.auth.forms import AuthenticationForm

@login_required(login_url="login")
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

@login_required(login_url="login")
@permission_required("meetups.add_meetup", login_url='/login', raise_exception=True)
def creator_panel_view(request, pk):
    user = User.objects.get(id=pk)
    meetups = Meetup.objects.filter(organizer=user)

    context = {
        "meetups":meetups,
        }

    return render(request, "meetups/creator_panel.html", context)


@login_required(login_url="login")
def detail_view(request, slug):
    error_message=None
    try:
        meetup = Meetup.objects.get(slug=slug)
        if request.method == "GET":
            form = ParticipantForm(initial={'email': request.user.email})
            print(request.method)

        else:
            form = ParticipantForm(request.POST, initial={'email': request.user.email})
            if form.is_valid():
                email = form.cleaned_data["email"]
                participant = User.objects.get(email=email)
                meetup.participants.add(participant)
                # messages.success(request, f"You have been successfully sing up for {meetup} meetup.")
                # print(messages)
                error_message = f"You have been successfully sing up for {meetup} meetup"
                print(error_message)
               

            else:
                # messages.error(request, "Ups Something something went wrong!")
                error_message = "Ups Something something went wrong"
            
        context = {
            "meetup":meetup,
            "meetup_exist":True,
            "form":form,
            "error_message":error_message
            
        }
        return render(request, "meetups/detail.html" ,context)
    
    except Exception as exc:

        context = {
            "meetup_exist":False
        }
        return render(request, "meetups/detail.html" ,context)

@login_required(login_url="login")
def all_meetups_view(request):
    meetups = Meetup.objects.all()

    context = {
        "meetups": meetups,
    }

    return render(request, "meetups/all_meetups.html", context)

@login_required(login_url="login")
@permission_required("meetups.change_meetup", login_url='/login', raise_exception=True)
def update_meetup_view(request, slug):
    user = request.user
    meetup = Meetup.objects.get(slug=slug)
    locations = Location.objects.all()

    if meetup.organizer != user:
        return HttpResponse("You not allowed hear!")
    
    if request.method == "POST":
        form = MeetupForm(request.POST, request.FILES, instance=meetup)
        if form.is_valid():
            meetup = form.save(commit=False)
            meetup.slug = slugify(meetup.title)
            meetup.organizer = request.user
            print(meetup.title)
            form.save()
            return redirect("creator-panel", pk=user.id)
    else:
        form = MeetupForm(instance=meetup)



    context={
        "meetup":meetup,
        "form": form,
        "locations": locations
    }
    return render(request, "meetups/update_meetup.html", context)


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
                meetup.organizer = request.user
                meetup.save()
                return redirect("home")
        else:
            form = MeetupForm()

    except ValidationError as err:
        form = MeetupForm()
        error_message = ", ".join(err)

        context = {
            "form" : form,
            "locations":locations,
            "error_message": error_message
        }
        return render(request, "meetups/create_meetup.html", context)

    context = {
        "form":form,
        "locations":locations,
        }

    return render(request, "meetups/create_meetup.html", context)



@login_required(login_url="login")
@permission_required('meetups.add_location', login_url='/login', raise_exception=True)
def add_new_location_view(request):
    print(request.method)
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data.get('city') 
            street = form.cleaned_data.get('street') 
            # print(city)
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
        if group:
            group_obj = Group.objects.get(name=group)
            user.groups.add(group_obj)
            user.save()
            return redirect("create-company", pk=pk)
        
    return render(request, "meetups/default_or_creator.html", {} )

def create_company_view(request, pk):
    if request.method == "POST":
        user = User.objects.get(id=pk)
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.creator = user
            company.save()
            return redirect("creator-panel", pk=pk)
    else:
        form = CompanyForm()
    
    context = {
        "form": form
    }

    return render(request, "meetups/create_company.html", context )
        

def login_view(request):
    error_message = None
    form = AuthenticationForm()

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


# ==== HTMX views ====

def get_last_location_view(request):
    last_loc = Location.objects.last()
    # html = "<div id='chosen_location' class='forms-control {% if field.errors %} errors {% endif %}' ><label>{{ form.location.label_tag }}</label>{{ form.location.errors }}{% render_field form.location class='form-control' }<button hx-get='/htmx/last_loc' hx-target='#dialog'  id='add_location' type='button' class='button-form mt-2' >Add new location</button></div>"
    html = "<label for='id_location'>Location:</label><select name='location' required id='id_location'><option value='%s' selected>%s</option></select>" %(last_loc.id,last_loc)
    return HttpResponse(html)
    # if request.method == 'POST':
    #     city = request.POST.get("city")
    #     street = request.POST.get("street")

    #     print(city)
    #     print(street)

    #     # Przykładowa logika obsługi danych i zapisywania do bazy danych
    #     # html = "<label for='id_location'>Location:</label><select name='location' required id='id_location'><option value='%s' selected>%s</option></select>" %(last_loc.id,last_loc)

    #     return HttpResponse(status=200)
  
def check_username_view(request):
    username = request.POST.get("username")
    if User.objects.filter(username=username).exists():
        return HttpResponse("<div id='username-error' class='error'>This username already exists</div>")
    else:
        return HttpResponse("<div id='username-error' class='success'>This username ia available</color=>")


@login_required(login_url="login")
@permission_required('meetups.delete_meetup', login_url='/login', raise_exception=True)
def delete_meetup_view(request, slug):
    user = request.user.id
    meetup = Meetup.objects.get(slug=slug)
    meetup.delete()

    meetups = Meetup.objects.filter(organizer=user)

    context = {
        "meetups":meetups,
        }
    return render(request, "meetups/includes/meetup-list.html", context )
    