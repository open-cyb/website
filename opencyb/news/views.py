from django.shortcuts import render, get_object_or_404
from .models import New
from .forms import CommentForm
import django.views.generic as generic
from django.http import HttpResponseRedirect
from django.contrib import messages

class NewsList(generic.ListView):
    queryset = New.objects.filter(status=1).order_by('-created_on')
    template_name = 'news_page.html'

class NewDetail(generic.DetailView):
    model = New
    template_name = 'new_detail.html'

def new_detail(request, slug):
    template_name = 'new_detail.html'
    new = get_object_or_404(New, slug=slug)
    comments = new.comments.filter(active=True)
    new_comment = None

    # Commend posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create comment object
            new_comment = comment_form.save(commit=False)
            # Assign the current new to the comment
            new_comment.new = new
            # Save the comment to the database
            new_comment.save()
            
            messages.success(request, "Ваш комментарий был отправлен на модерацию.")
            return HttpResponseRedirect(request.path)
    else:
        comment_form = CommentForm()
    
    return render(request, template_name, { 'new': new,
                                            'comments': comments,
                                            'new_comment': new_comment,
                                            'comment_form': comment_form })