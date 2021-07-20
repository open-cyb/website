from typing import Generic
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Photo
from .forms import PhotoForm
from django.utils.text import slugify
from unidecode import unidecode

def photos_list(request):
    template_name = 'gallery/gallery.html'
    context = {}
    queryset = Photo.objects.order_by('-created_on')
    context['photo_list'] = queryset

    return render(request, template_name, context)

def photo_upload(request):
    template_name = 'gallery/photo_upload.html'
    context = {}
    context['form'] = PhotoForm()

    if request.method == 'GET':
        return render(request, template_name, context)
    
    elif request.method == 'POST':
        upload_form = PhotoForm(request.POST, request.FILES)
        
        if upload_form.is_valid():  
            photo_object = upload_form.save()
            
            return HttpResponseRedirect(request.build_absolute_uri('/gallery/'))
        
        context['errors'] = upload_form.errors

        return render(request, template_name, context)