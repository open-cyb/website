from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, unique=True)
    # image = models.ImageField(blank=True)
    image = models.URLField(blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    links_json = models.TextField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"