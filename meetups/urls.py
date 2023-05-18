from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("<slug:slug>", views.detail_view, name="detail"),
    path("meetups/all-meetups", views.all_meetups_view, name="all-meetups"),
    path("meetups/search", views.search_meetups, name="search"),
    path("meetups/create", views.create_meetup_view, name="create-meetup"),
    path("meetups/create/location", views.add_new_location_view, name="create-location"),
    
    path("meetups/profile/sing-up",views.sign_up_user_view, name="sign-up"),
    path("meetups/profile/default-or-creator/<int:pk>", views.default_or_creator_view, name="default_or_creator"),
    path("meetups/profile/logout",views.logout_view, name="logout"),
    path("meetups/profile/login",views.login_view, name="login"),

]