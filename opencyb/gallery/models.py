from django.db import models
from django.contrib.auth.models import User
from opencyb import settings
import PIL
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

class Photo(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='gallery')
    photo = models.ImageField(upload_to='gallery/')
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
    
    def __str__(self):
        return "Title: {}. Description: {}. Slug: {}".format(self.title, self.description, self.slug)

    def save(self, *args, **kwargs):
        if not self.id:
            self.photo = self.compressImage(self.photo)
        super(Photo, self).save(*args, **kwargs)
    
    def compressImage(self,uploadedImage):
        imageTemproary = Image.open(uploadedImage)
        outputIoStream = BytesIO()
        imageTemproary.save(outputIoStream , format='JPEG', quality=60)
        outputIoStream.seek(0)
        uploadedImage = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % uploadedImage.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return uploadedImage