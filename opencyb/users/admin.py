from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug')
    prepopulated_fields = {'slug': ('user',)}

admin.site.register(Profile, ProfileAdmin)