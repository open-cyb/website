from django.contrib import admin
from .models import Shortener

class ShortenerAdmin(admin.ModelAdmin):
    list_display = ('short_url', 'long_url')

admin.site.register(Shortener, ShortenerAdmin)