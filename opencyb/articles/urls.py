from django.urls.resolvers import URLPattern
from . import views
from django.urls import path

urlpatterns = [
    path('', views.ArticlesList.as_view(), name='articles_page'),
    path('<slug:slug>/', views.ArticleDetail.as_view(), name='article_detail'),
]