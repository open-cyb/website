"""opencyb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.redirect_to_news),
    path('news/', include('news.urls')),
    path('projects/', include('projects.urls')),
    path('articles/', include('articles.urls')),
    # path('contacts/', TemplateView.as_view(template_name='contacts.html'), name='contacts_page'),
    path('search', views.search, name='search_page'),
    path('contacts/', include('users.urls')),
    path('gallery/', include('gallery.urls')),
    path('s/', include('urlshortener.urls')),
    path('snippets/', include('snippets.urls')),
] # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)