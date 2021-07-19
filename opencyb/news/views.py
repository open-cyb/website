from django.shortcuts import render, get_object_or_404
from .models import New
from .forms import NewForm, CommentForm
import django.views.generic as generic
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.text import slugify
from unidecode import unidecode

def news_list(request):
    template_name = 'news/news_page.html'
    context = {}
    queryset = New.objects.order_by('-created_on').filter(status=1)
    queryset_drafts_only = New.objects.filter(status=0)

    if request.method == 'GET':
        context['new_list'] = queryset
        context['posted'] = True
        return render(request, template_name, context)
    
    elif request.method == 'POST':
        n_select = request.POST.get('n_select')
        if n_select == 'Публикации':
            context['posted'] = True
            context['new_list'] = queryset
        elif n_select == 'Только черновики':
            context['drafts_only'] = True
            context['new_list'] = queryset_drafts_only
        
        return render(request, template_name, context)

def new_detail(request, slug):
    template_name = 'news/new_detail.html'
    new = get_object_or_404(New, slug=slug)
    comments = new.comments.filter(active=True)
    new_comment = None

    # Commend posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create comment object
            new_comment = comment_form.save(commit=False)
            # Assign the current new to the comment
            new_comment.new = new
            # Save the comment to the database
            new_comment.save()
            
            messages.success(request, "Ваш комментарий был отправлен на модерацию.")
            return HttpResponseRedirect(request.path)
    else:
        comment_form = CommentForm()
    
    return render(request, template_name, { 'new': new,
                                            'comments': comments,
                                            'new_comment': new_comment,
                                            'comment_form': comment_form })

def new_edit(request, slug):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(request.build_absolute_uri('/'))
    
    template_name = 'news/new_edit.html'
    context = {}
    edit_form = NewForm(instance = New.objects.get(slug=slug))
    context['form'] = edit_form

    if request.method == 'GET':
        return render(request, template_name, context)
    
    elif request.method == 'POST':
        instance = get_object_or_404(New, slug=slug)
        edit_form = NewForm(request.POST, instance=instance)

        if edit_form.is_valid():
            new_object = edit_form.save(commit=False)
            new_object.slug = slugify(unidecode(new_object.title))
            new_object.save()
            return HttpResponseRedirect(request.build_absolute_uri('/news/' + new_object.slug))
        
        context['errors'] = edit_form.errors

        return render(request, template_name, context)

def new_upload(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(request.build_absolute_uri('/'))
    
    template_name = 'news/new_upload.html'
    context = {}
    context['form'] = NewForm()

    if request.method == 'GET':
        return render(request, template_name, context)
    
    elif request.method == 'POST':
        a_form = NewForm(request.POST)

        if a_form.is_valid():
            new_object = a_form.save(commit=False)
            new_object.slug = slugify(unidecode(new_object.title))
            new_object.save()
            return HttpResponseRedirect(request.build_absolute_uri('/news/' + new_object.slug))
        
        context['errors'] = a_form.errors

        return render(request, template_name, context)