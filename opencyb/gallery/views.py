from typing import Generic
from django.shortcuts import render, get_object_or_404
from .models import Photo
import django.views.generic as generic

class PhotosList(generic.ListView):
    queryset = Photo.objects.order_by('-created_on')
    template_name = 'gallery/gallery.html'