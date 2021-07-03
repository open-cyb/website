from django.urls.resolvers import URLPattern
from . import views
from django.urls import path

urlpatterns = [
    path('', views.ProjectsList.as_view(), name='projects_page'),
    path('<slug:slug>/', views.ProjectDetail.as_view(), name='project_detail'),
]