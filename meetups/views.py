from django.shortcuts import render

def home_view(request):
    text = f"Hello from views.py"

    context = {
        "text":text
    }

    return render(request, "meetups/home.html", context)


def all_meetups_view(request):
    text = f"all meetups from views"

    context = {
        "text": text,
    }

    return render(request, "meetups/all_meetups.html", context)