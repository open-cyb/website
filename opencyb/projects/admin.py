from django.contrib import admin
from .models import Project, Comment

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_on')
    list_filter = ('status',)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'email', 'created_on', 'active')
    list_filter = ('active', 'created_on', 'project')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
    
    def hide_comments(self, request, queryset):
        queryset.update(active=False)

admin.site.register(Project, ProjectAdmin)
admin.site.register(Comment, CommentAdmin)