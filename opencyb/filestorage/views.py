from typing import Generic
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import File
from .forms import FileForm
from django.utils.text import slugify
from unidecode import unidecode
import os

def files_list(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(request.build_absolute_uri('/'))
    
    template_name = 'filestorage/files_list.html'
    context = {}
    queryset = File.objects.order_by('-created_on')
    context['file_list'] = queryset

    return render(request, template_name, context)

def file_upload(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(request.build_absolute_uri('/'))
    
    template_name = 'filestorage/file_upload.html'
    context = {}
    context['form'] = FileForm()

    if request.method == 'GET':
        return render(request, template_name, context)
    
    elif request.method == 'POST':
        upload_form = FileForm(request.POST, request.FILES)
        
        if upload_form.is_valid():  
            file_object = upload_form.save(commit=False)
            file_object.save()
            
            return HttpResponseRedirect(request.build_absolute_uri('/filestorage/'))
        
        context['errors'] = upload_form.errors

        return render(request, template_name, context)

def redirect_url_view(request, slug):
    return HttpResponseRedirect(get_object_or_404(File, slug=slug).file.url)

def file_edit(request, slug):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(request.build_absolute_uri('/'))
    
    template_name = 'filestorage/file_edit.html'
    context = {}
    context['form'] = FileForm(instance = File.objects.get(slug=slug))

    if request.method == 'GET':
        return render(request, template_name, context)
    
    elif request.method == 'POST':
        instance = get_object_or_404(File, slug=slug)
        edit_form = FileForm(request.POST, request.FILES, instance=instance)
        
        if edit_form.is_valid():
            if len(request.FILES) != 0: # Если в форму загружен файл, то прежний удалить из media/filestorage/ перед загрузкой нового
                os.remove(os.path.dirname(instance.file.path) + '/filestorage/' + os.path.basename(File.objects.get(slug=slug).file.name))
            file_object = edit_form.save(commit=False)
            file_object.save()
            
            return HttpResponseRedirect(request.build_absolute_uri('/filestorage/'))
        
        context['errors'] = edit_form.errors

        return render(request, template_name, context)