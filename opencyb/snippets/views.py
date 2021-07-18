from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
import django.views.generic as generic
from .models import Snippet
from .forms import SnippetForm

def snippets_list(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(request.build_absolute_uri('/'))
    
    template_name = 'snippets/snippets_page.html'
    context = {}
    queryset = Snippet.objects.order_by('-created_on')

    if request.method == 'GET':
        context['snippet_list'] = queryset
        return render(request, template_name, context)
    
    elif request.method == 'POST':
        filtered = request.POST['filtered']
        if filtered == '':
            queryset = Snippet.objects.order_by('-created_on')
        else:
            queryset = Snippet.objects.filter(title__contains=filtered)
            if len(queryset) == 0:
                context['filtered_not_results'] = True
        
        context['snippet_list'] = queryset
        return render(request, template_name, context)

def snippet_detail(request, slug):
    template_name = 'snippets/snippet_detail.html'
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
        return HttpResponseRedirect(request.build_absolute_uri('/'))

    template_name = 'snippets/snippet_upload.html'

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

def snippet_edit(request, slug):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(request.build_absolute_uri('/'))
    
    template_name = 'snippets/snippet_edit.html'

    context = {}

    edit_form = SnippetForm(instance = Snippet.objects.get(slug=slug))
    context['form'] = edit_form

    if request.method == 'GET':
        return render(request, template_name, context)
    
    elif request.method == 'POST':
        instance = get_object_or_404(Snippet, slug=slug)
        edit_form = SnippetForm(request.POST, instance=instance)

        if edit_form.is_valid():
            snippet_object = edit_form.save()
            return HttpResponseRedirect(request.build_absolute_uri('/snippets/' + snippet_object.slug))
        
        context['errors'] = edit_form.errors

        return render(request, template_name, context)