from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
import django.views.generic as generic
from .models import Snippet
from .forms import SnippetForm

class SnippetsList(generic.ListView):
    queryset = Snippet.objects.order_by('-created_on')
    template_name = 'snippets_app/snippets_page.html'

def snippet_detail(request, slug):
    template_name = 'snippets_app/snippet_detail.html'
    snippet = get_object_or_404(Snippet, slug=slug)
    
    context = {
        'snippet': snippet
    }

    code = snippet.code
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import HtmlFormatter
    lexer = get_lexer_by_name(str(snippet.language).lower(), stripall=True)
    formatter = HtmlFormatter(linenos=True, cssclass='codehilite')
    result = highlight(code, lexer, formatter)
    context['code'] = result
    

    return render(request, template_name, context)

def snippet_upload(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(request.build_absolute_uri('/snippets/'))

    template_name = 'snippets_app/snippet_upload.html'

    context = {}

    context['form'] = SnippetForm()

    if request.method == 'GET':
        return render(request, template_name, context)
        
    elif request.method == 'POST':
        user_form = SnippetForm(request.POST)

        if user_form.is_valid():
            snippet_object = user_form.save()
            return HttpResponseRedirect(request.build_absolute_uri('/snippets/' + snippet_object.slug))
        
        context['errors'] = user_form.errors

        return render(request, template_name, context)