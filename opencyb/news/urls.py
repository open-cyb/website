from django.urls.resolvers import URLPattern
from . import views
from django.urls import path

urlpatterns = [
    path('', views.news_list, name='home'),
    path('upload/', views.new_upload, name='new_upload'),
    path('<slug:slug>/', views.new_detail, name='new_detail'),
    path('<slug:slug>/edit/', views.new_edit, name='new_edit')
]