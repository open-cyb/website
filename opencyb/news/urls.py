from django.urls.resolvers import URLPattern
from . import views
from django.urls import path

urlpatterns = [
    path('', views.NewsList.as_view(), name='home'),
    path('<slug:slug>/', views.NewDetail.as_view(), name='new_detail'),
]