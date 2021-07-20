from django.db import models
from .utils import create_shortened_url
from django.contrib.auth.models import User

class Snippet(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=15, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='snippets')
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    code = models.TextField()
    language = models.CharField(max_length=200)

    class Meta:
        ordering = ['-created_on']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_shortened_url(self)
        
        super().save(*args, **kwargs)