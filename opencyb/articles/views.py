from django.shortcuts import render, get_object_or_404
from .models import Article
from .forms import ArticleForm, CommentForm
import django.views.generic as generic
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.text import slugify
from unidecode import unidecode

class ArticlesList(generic.ListView):
    queryset = Article.objects.filter(status=1).order_by('-created_on')
    template_name = 'articles/articles_page.html'

def article_detail(request, slug):
    template_name = 'articles/article_detail.html'
    article = get_object_or_404(Article, slug=slug)
    comments = article.comments.filter(active=True)
    new_comment = None

    # Commend posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create comment object
            new_comment = comment_form.save(commit=False)
            # Assign the current article to the comment
            new_comment.article = article
            # Save the comment to the database
            new_comment.save()
            
            messages.success(request, "Ваш комментарий был отправлен на модерацию.")
            return HttpResponseRedirect(request.path)
    else:
        comment_form = CommentForm()
    
    return render(request, template_name, { 'article': article,
                                            'comments': comments,
                                            'new_comment': new_comment,
                                            'comment_form': comment_form })

def article_edit(request, slug):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(request.build_absolute_uri('/'))
    
    template_name = 'articles/article_edit.html'
    context = {}
    edit_form = ArticleForm(instance = Article.objects.get(slug=slug))
    context['form'] = edit_form

    if request.method == 'GET':
        return render(request, template_name, context)
    
    elif request.method == 'POST':
        instance = get_object_or_404(Article, slug=slug)
        edit_form = ArticleForm(request.POST, instance=instance)

        if edit_form.is_valid():
            article_object = edit_form.save(commit=False)
            article_object.slug = slugify(unidecode(article_object.title))
            article_object.save()
            return HttpResponseRedirect(request.build_absolute_uri('/articles/' + article_object.slug))
        
        context['errors'] = edit_form.errors

        return render(request, template_name, context)

def article_upload(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(request.build_absolute_uri('/'))
    
    template_name = 'articles/article_upload.html'
    context = {}
    context['form'] = ArticleForm()

    if request.method == 'GET':
        return render(request, template_name, context)
    
    elif request.method == 'POST':
        a_form = ArticleForm(request.POST)

        if a_form.is_valid():
            article_object = a_form.save(commit=False)
            article_object.slug = slugify(unidecode(article_object.title))
            article_object.save()
            return HttpResponseRedirect(request.build_absolute_uri('/articles/' + article_object.slug))
        
        context['errors'] = a_form.errors

        return render(request, template_name, context)