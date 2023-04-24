from django.urls import path

from .views import home_view, all_meetups_view, detail_view

urlpatterns = [
    path("", view=home_view, name="home"),
    path("all-meetups", view=all_meetups_view, name="all_meetups"),
    path("/<slug:slug>", view=detail_view, name="detail")
]