from django.urls import path
from . import views

urlpatterns = [
    path("", views.SnippetsList.as_view(), name="snippets_page"),
    path("upload/", views.snippet_upload, name="snippet_upload"),
    path("<slug:slug>/", views.snippet_detail, name='snippet_detail')
]
