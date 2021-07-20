from django.urls.resolvers import URLPattern
from . import views
from django.urls import path

urlpatterns = [
    path('', views.files_list, name='filestorage_files_list'),
    path('upload/', views.file_upload, name='filestorage_file_upload'),
    path("<slug:slug>", views.redirect_url_view, name='filestorage_redirect'),
    path("<slug:slug>/edit/", views.file_edit, name='filestorage_file_edit'),
    path("<slug:slug>/delete/", views.file_delete, name='filestorage_file_delete'),
]