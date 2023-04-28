from django.test import TestCase
from django.urls import reverse, resolve
from django.utils import timezone

import datetime

from .views import home_view, detail_view
from .models import Meetup, Location

class HomePageTest(TestCase):
    def setUp(self) -> None:
        url = reverse("home")
        self.response = self.client.get(url)

    def test_url_exists_at_correct_location(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_templates(self):
        self.assertTemplateUsed(self.response, "meetups/home.html")
        
    def test_templates_contain_correct_html(self):
        self.assertContains(self.response, "Latest meetups")

    def test_homepage_resolve_home_page_view(self):
        view = resolve("/")
        self.assertEqual(view.func.__name__, home_view.__name__)
    


class MeetupsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.location = Location.objects.create(country="Poland",
                                               city="Warsaw",
                                               street="Main Street")
        
        cls.meetup = Meetup.objects.create(title="test meetup",
                              description="test meetup description",
                              organizer_email="test@email.com",
                              image="test.jpg",
                              date=timezone.now().date() + datetime.timedelta(days=1),
                              slug='test-slug',
                              location = cls.location)
        
    
    def test_meetup_model(self):
        meetup = Meetup.objects.first()
        self.assertEqual(Meetup.objects.all().count(), 1)
        self.assertEqual(self.meetup.title, "test meetup")
        self.assertEqual(meetup.description, "test meetup description")
        self.assertEqual(meetup.organizer_email, "test@email.com")
        self.assertEqual(meetup.location.country, "Poland")
        self.assertEqual(meetup.location.city, "Warsaw")
        self.assertEqual(meetup.location.street, "Main Street")
        self.assertIsInstance(meetup.date, datetime.date)
        self.assertAlmostEqual(
            meetup.created,
            timezone.now(),
            delta=datetime.timedelta(seconds=1),
        )

    def test_detail_view(self):
        response = self.client.get(self.meetup.get_absolute_url())
        no_response = self.client.get("/wrong-slug/")
        view =  resolve("/test-slug")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "test meetup")
        self.assertTemplateUsed(response, "meetups/detail.html")
        self.assertEqual(view.func.__name__, detail_view.__name__)
    

    def test_all_meetups_view(self):
        response = self.client.get(reverse("all_meetups"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "meetups/all_meetups.html")

    def test_search_meetups_view(self):
        response = self.client.get(reverse("search"), {"q":"test"})
        country_response = self.client.get(reverse("search"), {"q":"poland"})
        no_response = self.client.get(reverse("search"), {"q":"no response"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 200)
        self.assertEqual(country_response.status_code, 200)
        self.assertContains(response, "test meetup")
        self.assertContains(country_response, "Poland")
        self.assertNotContains(response, "Something else")
        self.assertNotContains(no_response, "test meetup")
        self.assertTemplateUsed(response, "meetups/search.html")
        self.assertTemplateUsed(no_response, "meetups/search.html")
        self.assertTemplateUsed(country_response, "meetups/search.html")


