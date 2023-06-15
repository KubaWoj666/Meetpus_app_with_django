
from django.contrib.sessions.models import Session

def count_views_by_meetup(meetups):
    views_by_meetup = {}
    for meetup in meetups:
        views_by_meetup[meetup.slug] = 0 
    
        for session in Session.objects.all():
            session_data = session.get_decoded()
            print(session_data)
            
            if meetup.slug in session_data.keys():
                views = session_data.get(meetup.slug, 0)
                print(views)
               
                views_by_meetup[meetup.slug] += views  
    return views_by_meetup