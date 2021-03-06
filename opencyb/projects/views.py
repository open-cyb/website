from django.shortcuts import render, get_object_or_404
from .models import Project
from .forms import CommentForm
import django.views.generic as generic
from django.http import HttpResponseRedirect
from django.contrib import messages

class ProjectsList(generic.ListView):
    queryset = Project.objects.filter(status=1).order_by('-created_on')
    template_name = 'projects/projects_page.html'

def project_detail(request, slug):
    template_name = 'projects/project_detail.html'
    project = get_object_or_404(Project, slug=slug)
    comments = project.comments.filter(active=True)
    new_comment = None

    # Commend posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create comment object
            new_comment = comment_form.save(commit=False)
            # Assign the current article to the comment
            new_comment.project = project
            # Save the comment to the database
            new_comment.save()

            messages.success(request, "Ваш комментарий был отправлен на модерацию.")
            return HttpResponseRedirect(request.path)
    else:
        comment_form = CommentForm()
    
    return render(request, template_name, { 'project': project,
                                            'comments': comments,
                                            'new_comment': new_comment,
                                            'comment_form': comment_form })