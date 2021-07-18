from django.shortcuts import render, redirect
from news.models import New
from articles.models import Article
from projects.models import Project

def redirect_to_news(request):
    response = redirect('/news/')
    return response

def search(request):
    template_name = 'search/search_page.html'
    
    if request.method == "POST":
        searched = request.POST['searched']
        
        news_results = New.objects.filter(title__contains=searched) | New.objects.filter(content__contains=searched)
        projects_results = Project.objects.filter(title__contains=searched) | Project.objects.filter(content__contains=searched)
        articles_results = Article.objects.filter(title__contains=searched) | Article.objects.filter(content__contains=searched)
        
        context = {}
        context['searched'] = searched
        context['news_results'] = news_results
        context['projects_results'] = projects_results
        context['articles_results'] = articles_results

        return render(request, template_name, context)
    else:
        return render(request, template_name, {})