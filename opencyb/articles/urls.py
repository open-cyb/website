from django.urls.resolvers import URLPattern
from . import views
from django.urls import path

urlpatterns = [
    path('', views.ArticlesList.as_view(), name='articles_page'),
    path('upload/', views.article_upload, name='article_upload'),
    path('<slug:slug>/', views.article_detail, name='article_detail'),
    path('<slug:slug>/edit/', views.article_edit, name='article_edit'),
]