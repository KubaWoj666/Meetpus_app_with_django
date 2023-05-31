from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.core.exceptions import ValidationError

import datetime

class Company(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    # NIP = models.IntegerField(max_length=10)
    creator = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self) -> str:
        return self.name




class Location(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=200)
    street = models.CharField(max_length=300)

    def __str__(self) -> str:
        return f"{self.city} - {self.street}"



class Meetup(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="images")
    organizer_email = models.EmailField()
    date = models.DateField()
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, blank=True, null=True, related_name="participants")
    
    

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('detail', args=[self.slug])
    
    def save(self, *args, **kwargs) -> None:
        if self.date < datetime.date.today():
            raise ValidationError("The date cannot be in the past")
        return super().save(*args, **kwargs)