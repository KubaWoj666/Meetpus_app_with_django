from django.contrib import admin
from .models import Meetup, Location


class AdminMeetup(admin.ModelAdmin):
    list_display = ["title", "date", "created", "location"]
    prepopulated_fields = {"slug":["title"]}
    list_filter = ("date", "title")


admin.site.register(Meetup, AdminMeetup)
admin.site.register(Location)

