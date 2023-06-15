from django import template

register = template.Library()

def get_meetup_views(meetup_views, meetup_slug):
    return meetup_views.get(meetup_slug, 0)
register.filter("get_views", get_meetup_views)