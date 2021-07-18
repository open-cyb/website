from django.shortcuts import render, get_object_or_404
from .models import Article
from .forms import CommentForm
import django.views.generic as generic
from django.http import HttpResponseRedirect
from django.contrib import messages

class ArticlesList(generic.ListView):
    queryset = Article.objects.filter(status=1).order_by('-created_on')
    template_name = 'articles/articles_page.html'

def article_detail(request, slug):
    template_name = 'articles/article_detail.html'
    article = get_object_or_404(Article, slug=slug)
    comments = article.comments.filter(active=True)
    new_comment = None

    # Commend posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create comment object
            new_comment = comment_form.save(commit=False)
            # Assign the current article to the comment
            new_comment.article = article
            # Save the comment to the database
            new_comment.save()
            
            messages.success(request, "Ваш комментарий был отправлен на модерацию.")
            return HttpResponseRedirect(request.path)
    else:
        comment_form = CommentForm()
    
    return render(request, template_name, { 'article': article,
                                            'comments': comments,
                                            'new_comment': new_comment,
                                            'comment_form': comment_form })