from django.urls import path

from .views import home_view, all_meetups_view, detail_view, search_meetups

urlpatterns = [
    path("", view=home_view, name="home"),
    path("<slug:slug>", view=detail_view, name="detail"),
    path("meetups/all-meetups", view=all_meetups_view, name="all_meetups"),
    path("meetups/search", view=search_meetups, name="search")
    
]