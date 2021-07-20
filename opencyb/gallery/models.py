from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from opencyb import settings
import PIL
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
import os
from .utils import create_shortened_url
from cv2 import cv2
import numpy as np

class Photo(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='gallery')
    photo = models.FileField(upload_to='gallery/')
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
    
    def __str__(self):
        return "Title: {}. Description: {}. Slug: {}".format(self.title, self.description, self.slug)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_shortened_url(self)
        if not self.id:
            self.photo = self.compressImage(self.photo)
        super(Photo, self).save(*args, **kwargs)
    
    def compressImage(self, uploadedImage):
        img_temp = Image.open(uploadedImage).convert('RGB')
        img = cv2.cvtColor(np.asarray(img_temp),cv2.COLOR_RGB2BGR)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        result, encimg = cv2.imencode('.jpg', img, encode_param)
        outputIoStream = BytesIO(encimg)
        uploadedImage = InMemoryUploadedFile(outputIoStream, 'FileField', "%s.jpg" % self.slug, 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return uploadedImage

# Удалить файл, если удаляется модель
@receiver(models.signals.post_delete, sender=Photo)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.photo:
        if os.path.isfile(instance.photo.path):
            os.remove(instance.photo.path)