from django.urls import path
from .views import home_view, redirect_url_view

urlpatterns = [
    path("", home_view, name="urlshortener_home"),
    path("<str:shortened_part>", redirect_url_view, name='redirect')
]
