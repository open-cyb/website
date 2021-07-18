from django.urls import path
from .views import shorteners_page, shortener_upload, redirect_url_view

urlpatterns = [
    path("", shorteners_page, name="shorteners_page"),
    path("upload/", shortener_upload, name="shortener_upload_page"),
    path("<str:shortened_part>", redirect_url_view, name='redirect')
]
