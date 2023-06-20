from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("<slug:slug>", views.detail_view, name="detail"),
    path("meetups/all-meetups", views.all_meetups_view, name="all-meetups"),
    path("meetups/search", views.search_meetups, name="search"),
    path("meetups/create", views.create_meetup_view, name="create-meetup"),
    path("meetup/read-later", views.ReadLater.as_view(), name="read-later"),
    path("meetups/create/location", views.add_new_location_view, name="create-location"),
    path("meetups/my-meetups/<int:pk>", views.user_sign_up_meetups_view, name="my_meetups"),
     
    path("meetups/profile/sing-up",views.sign_up_user_view, name="sign-up"),
    path("meetups/profile/default-or-creator/<int:pk>", views.default_or_creator_view, name="default_or_creator"),
    path("meetups/profile/company-info/<int:pk>", views.create_company_view, name="create-company"),
    path("meetups/profile/logout",views.logout_view, name="logout"),
    path("meetups/profile/login",views.login_view, name="login"),

    path("meetups/creator-panel/<int:pk>", views.creator_panel_view, name="creator-panel"),
    path("meetups/update-meetup/<slug:slug>", views.update_meetup_view, name="update_meetup"),
]

htmx_urlpatterns = [
    path("htmx/last_loc", views.get_last_location_view, name="last_location"),
    path("htmx/check_username", views.check_username_view, name="check-username"),
    path("htmx/delete-meetup/<slug:slug>", views.delete_meetup_view, name="delete_meetup"),
    path("htmx/remove-meetup-from-session/<slug:slug>", views.remove_form_session, name="remove_meetup_from_session"),
    # path("htmx/like-meetup/<slug:slug>", views.like_meetup_view, name="like")
]

urlpatterns += htmx_urlpatterns