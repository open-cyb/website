from django.shortcuts import render
from .models import New
import django.views.generic as generic

class NewsList(generic.ListView):
    queryset = New.objects.filter(status=1).order_by('-created_on')
    template_name = 'news_page.html'

class NewDetail(generic.DetailView):
    model = New
    template_name = 'new_detail.html'