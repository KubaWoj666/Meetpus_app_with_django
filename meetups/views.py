from django.shortcuts import render

from.models import Meetup

def home_view(request):
    meetups = Meetup.objects.all()
    latest_meetups = meetups.order_by("-created")[:3]
    

    context = {
        "latest_meetups": latest_meetups
    }

    return render(request, "meetups/home.html", context)


def detail_view(request, slug):
    meetup = Meetup.objects.get(slug=slug)

    context = {
        "meetup":meetup
    }
    return render(request, "meetups/detail.html" ,context)


def all_meetups_view(request):
    text = f"all meetups from views"

    context = {
        "text": text,
    }

    return render(request, "meetups/all_meetups.html", context)