from django.urls.resolvers import URLPattern
from . import views
from django.urls import path

urlpatterns = [
    path('', views.photos_list, name='gallery'),
    path('upload/', views.photo_upload, name='photo_upload')
]