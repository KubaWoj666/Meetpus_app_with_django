from django.contrib import admin
from .models import Meetup


class AdminMeetup(admin.ModelAdmin):
    list_display = ["title", "date", "created"]
    prepopulated_fields = {"slug":["title"]}
    list_filter = ("date",)


admin.site.register(Meetup, AdminMeetup)

