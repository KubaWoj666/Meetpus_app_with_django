from django.test import TestCase
from django.urls import reverse, resolve
from django.utils import timezone


import datetime

from .views import home_view, detail_view
from .models import Meetup

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
        cls.meetup = Meetup.objects.create(title="test meetup",
                              description="test meetup description",
                              organizer_email="test@email.com",
                              image="test.jpg",
                              date=timezone.now().date() + datetime.timedelta(days=1),
                              slug='test-slug')
    
    def test_meetup_model(self):
        meetup = Meetup.objects.first()
        self.assertEqual(Meetup.objects.all().count(), 1)
        self.assertEqual(self.meetup.title, "test meetup")
        self.assertEqual(meetup.description, "test meetup description")
        self.assertEqual(meetup.organizer_email, "test@email.com")
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
    