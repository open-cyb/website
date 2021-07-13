from django.urls.resolvers import URLPattern
from . import views
from django.urls import path

urlpatterns = [
    path('', views.profiles_page, name='contacts_page'),
    path('<slug:slug>/', views.profile_detail, name='profile_detail')
]