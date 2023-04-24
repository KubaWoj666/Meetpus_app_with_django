from django.db import models

class Meetup(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="images")
    organizer_email = models.EmailField()
    date = models.DateField()
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.title}"
