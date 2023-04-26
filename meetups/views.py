from django.shortcuts import render

from.models import Meetup

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
    meetup = Meetup.objects.get(slug=slug)

    context = {
        "meetup":meetup
    }
    return render(request, "meetups/detail.html" ,context)


def all_meetups_view(request):
    meetups = Meetup.objects.all()

    context = {
        "meetups": meetups,
    }

    return render(request, "meetups/all_meetups.html", context)