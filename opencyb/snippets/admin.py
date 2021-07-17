from django.contrib import admin
from .models import Snippet

class SnippetAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'slug', 'created_on')

admin.site.register(Snippet, SnippetAdmin)