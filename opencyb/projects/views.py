from django.shortcuts import render
from .models import Project
import django.views.generic as generic

class ProjectsList(generic.ListView):
    queryset = Project.objects.filter(status=1).order_by('-created_on')
    template_name = 'projects_page.html'

class ProjectDetail(generic.DetailView):
    model = Project
    template_name = 'project_detail.html'