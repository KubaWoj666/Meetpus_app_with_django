from django.contrib import admin
from .models import Meetup, Location

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User,Group

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'group_name')
    def group_name(self, obj):
        return obj.groups.first().name if obj.groups.exists() else ''
    group_name.short_description = 'Group'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)



class AdminMeetup(admin.ModelAdmin):
    list_display = ["title", "date", "created", "location"]
    prepopulated_fields = {"slug":["title"]}
    list_filter = ("date", "title")


admin.site.register(Meetup, AdminMeetup)
admin.site.register(Location)


