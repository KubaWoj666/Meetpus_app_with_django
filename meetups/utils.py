
from django.contrib.sessions.models import Session

def count_views_by_meetup(meetups):
    views_by_meetup = {}
    for meetup in meetups:
        views_by_meetup[meetup.slug] = 0 
    
        for session in Session.objects.all():
            session_data = session.get_decoded()
    
            if meetup.slug in session_data.keys():
                views = session_data.get(meetup.slug, 0)
                
               
                views_by_meetup[meetup.slug] += views  
    return views_by_meetup

def count_likes(meetups):
    likes_by_meetup = {meetup.slug: meetup.like_set.filter(meetup=meetup, liked=True).count() for meetup in meetups }
    return likes_by_meetup
