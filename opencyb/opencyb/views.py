from django.shortcuts import render, redirect
from news.models import New
from articles.models import Article
from projects.models import Project

def redirect_to_news(request):
    response = redirect('/news/')
    return response

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        #search_results = New.objects.filter(content__contains=searched) + New.objects.filter(content_contains=searched) + Article.objects.filter(content__contains=searched) + Article.objects.filter(content_contains=searched) + Project.objects.filter(content__contains=searched) + Project.objects.filter(content_contains=searched)
        news_results = New.objects.filter(title__contains=searched) | New.objects.filter(content__contains=searched)
        projects_results = Project.objects.filter(title__contains=searched) | Project.objects.filter(content__contains=searched)
        articles_results = Article.objects.filter(title__contains=searched) | Article.objects.filter(content__contains=searched)
        return render(request,
            'search_page.html',
            {'searched': searched,
            'news_results': news_results,
            'projects_results': projects_results,
            'articles_results': articles_results})
    else:
        return render(request,
            'search_page.html',
            {})