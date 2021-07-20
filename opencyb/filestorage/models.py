from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from .utils import create_shortened_url
import os
from django.utils.text import slugify
from unidecode import unidecode

class File(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='filestorage')
    file = models.FileField(upload_to='filestorage/')
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_shortened_url(self)
        file_ext = self.file.name.split('.')[-1]
        # self.file.name = slugify(unidecode(self.title)) + '.' + file_ext
        super(File, self).save(*args, **kwargs)
    
    def __str__(self):
        return ""

# Удалить файл, если удаляется модель
@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)