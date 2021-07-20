from django.urls import path
from . import views

urlpatterns = [
    path("", views.snippets_list, name="snippets_page"),
    path("upload/", views.snippet_upload, name="snippet_upload"),
    path("<slug:slug>/", views.snippet_detail, name='snippet_detail'),
    path("<slug:slug>/edit/", views.snippet_edit, name='snippet_edit'),
    path("<slug:slug>/delete/", views.snippet_delete, name='snippet_delete'),
]
