from django import template

register = template.Library()

def get_meetup_views(meetup_views, meetup_slug):
    return meetup_views.get(meetup_slug, 0)
register.filter("get_views", get_meetup_views)


def get_likes(likes_by_meetup, meetup_slug):
    return likes_by_meetup.get(meetup_slug, 0)
register.filter("get_likes", get_likes)