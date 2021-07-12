from django.contrib import admin
from .models import New, Comment

class NewAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_on')
    list_filter = ('status',)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'new', 'email', 'created_on', 'active')
    list_filter = ('active', 'created_on', 'new')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
    
    def hide_comments(self, request, queryset):
        queryset.update(active=False)

admin.site.register(New, NewAdmin)
admin.site.register(Comment, CommentAdmin)