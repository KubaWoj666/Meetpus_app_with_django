from django.shortcuts import render, get_object_or_404
from django.db.models import Q

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

    