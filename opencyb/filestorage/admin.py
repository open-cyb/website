from django.contrib import admin
from .models import File

class FileAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'created_on')
    prepopulated_fields = {'slug': ('title', )}

admin.site.register(File, FileAdmin)