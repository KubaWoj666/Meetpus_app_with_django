from django.test import TestCase
from django.urls import reverse, resolve
from django.utils import timezone
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.forms import AuthenticationForm



import datetime

from .views import home_view, detail_view
from .models import Meetup, Location

# class HomePageTest(TestCase):
#     def setUp(self) -> None:
#         url = reverse("home")
#         self.response = self.client.get(url)
    
#     @classmethod
#     def setUpTestData(cls):
#         cls.creator = User.objects.create_user(username="creator", 
#                                                email="creator@email.com", 
#                                                password="testpassword")
#         permission = Permission.objects.get(codename="add_meetup")
#         delete_permission = Permission.objects.get(codename="delete_meetup")
#         cls.creator.user_permissions.add(permission)
#         cls.creator.user_permissions.add(delete_permission)
    

#     # def test_url_exists_at_correct_location(self):
#     #     self.assertEqual(self.response.status_code, 200)

#     def test_homepage_templates(self):
#         self.client.login(username="creator", password="testpassword")
#         self.assertTemplateUsed(self.response, "meetups/home.html")
        
#     def test_templates_contain_correct_html(self):
#         self.assertContains(self.response, "Latest meetups")

#     def test_homepage_resolve_home_page_view(self):
#         view = resolve("/")
#         self.assertEqual(view.func.__name__, home_view.__name__)
    


class MeetupsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.creator = User.objects.create_user(username="creator", 
                                               email="creator@email.com", 
                                               password="testpassword")
        permission = Permission.objects.get(codename="add_meetup")
        delete_permission = Permission.objects.get(codename="delete_meetup")
        update_permission = Permission.objects.get(codename="change_meetup")
        cls.creator.user_permissions.add(permission)
        cls.creator.user_permissions.add(delete_permission, update_permission)
    

        cls.participant = User.objects.create_user(username="test", 
                                                   email="testuser@email.com",
                                                   password="testpassword")


        cls.location = Location.objects.create(country="Poland",
                                               city="Warsaw",
                                               street="Main Street")
        
        cls.meetup = Meetup.objects.create(title="test meetup",
                              description="test meetup description",
                              organizer_email="test@email.com",
                              image="test.jpg",
                              date=timezone.now().date() + datetime.timedelta(days=1),
                              slug='test-slug',
                              location = cls.location,
                              organizer=cls.creator)
        

    
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
    
    def test_create_meetups_view_with_permission(self):
        self.client.login(username="creator", password="testpassword")
        response = self.client.get(reverse("create-meetup"))
        self.assertEqual(response.status_code, 200)

    
    def test_create_meetups_view_without_permission(self):
        self.client.login(username="test", password="testpassword")
        response = self.client.get(reverse("create-meetup"))
        self.assertEqual(response.status_code, 403)
    

    def test_create_meetup_view_post_request(self):
        self.client.login(username="creator", password="testpassword")
        url = reverse("create-meetup")
        data = {"title":self.meetup.title,
                "description": self.meetup.description,
                "organizer_email":self.meetup.organizer_email,
                # "image":self.meetup.image,
                "date":self.meetup.date,
                "slug":self.meetup.slug,
                "location":self.meetup.location}
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)  
        self.assertTemplateUsed(response, "meetups/create_meetup.html")
        self.assertEqual(Meetup.objects.count(), 1)
        meetup = Meetup.objects.first()
        self.assertEqual(meetup.title, self.meetup.title)
        self.assertEqual(meetup.description, self.meetup.description)

  

    def test_detail_view(self):
        self.client.login(username="creator", password="testpassword")
        response = self.client.get(self.meetup.get_absolute_url())
        no_response = self.client.get("/wrong-slug/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "test meetup")
        self.assertTemplateUsed(response, "meetups/detail.html")


    def test_all_meetups_view(self):
        self.client.login(username="creator", password="testpassword")
        response = self.client.get(reverse("all-meetups"))
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


    def test_sing_up_view(self):
        url = reverse("sign-up")
        data = {"username":self.creator.username,
                "email":self.creator.email,
                "password1":self.creator.password,
                "password2":self.creator.password}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 2)
        self.assertTemplateUsed(response, "meetups/sign_up_user.html")


    def test_login_view_with_valid_credentials(self):
        url = reverse("login")
        data = {
            "username": self.creator.username,
            "password": self.creator.password,
        }
        response = self.client.post(url, data)
        user = get_user_model().objects.get(username=self.creator.username)
        self.assertTrue(user.is_authenticated)
        self.assertTemplateUsed(response, "meetups/login.html")
    

    def test_login_view_with_invalid_credentials(self):
        url = reverse("login")
        data = {
            "username": self.creator.username,
            "password": "wrongpassword",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed(response, "meetups/login.html")
        error_message = response.context["error_message"]
        self.assertEqual(error_message, "Invalid credentials")
        self.assertTemplateUsed(response, "meetups/login.html")

    def test_update_view_with_permission(self):
        self.client.login(username="creator", password="testpassword")
        url = reverse("update_meetup", args=[self.meetup.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "meetups/update_meetup.html")

        form_data = {"title":"updated title",
            "description":"test meetup description",
            "organizer_email":"test@email.com",
            "image":"test.jpg",
            "date":timezone.now().date() + datetime.timedelta(days=1),
            "slug":'updated-title',
            "location": self.location,
            "organizer": self.creator,
        }

        response = self.client.post(url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Meetup.objects.filter(slug='test-slug').exists())

    
    def test_delete_view_with_permission(self):
        self.client.login(username="creator", password="testpassword")
        response = self.client.delete(reverse("delete_meetup", args=[self.meetup.slug])) 
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Meetup.objects.filter(slug='updated-meetup-title').exists())


