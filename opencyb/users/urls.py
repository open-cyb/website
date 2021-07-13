from django.urls.resolvers import URLPattern
from . import views
from django.urls import path

urlpatterns = [
    path('<slug:slug>/', views.profile_detail, name='profile_detail')
]