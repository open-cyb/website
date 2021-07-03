from django.shortcuts import render
from .models import Article
import django.views.generic as generic

class ArticlesList(generic.ListView):
    queryset = Article.objects.filter(status=1).order_by('-created_on')
    template_name = 'articles_page.html'

class ArticleDetail(generic.DetailView):
    model = Article
    template_name = 'article_detail.html'