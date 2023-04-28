from django.urls import path

from .views import home_view, all_meetups_view, detail_view, search_meetups, create_meetup_view ,sign_up_view

urlpatterns = [
    path("", view=home_view, name="home"),
    path("<slug:slug>", view=detail_view, name="detail"),
    path("meetups/all-meetups", view=all_meetups_view, name="all-meetups"),
    path("meetups/search", view=search_meetups, name="search"),
    path("meetups/create", view=create_meetup_view, name="create-meetup"),
    path("meetups/profile/sing-up",view=sign_up_view, name="sign-up")
    
]