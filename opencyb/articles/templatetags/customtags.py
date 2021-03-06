from django import template
from bs4 import BeautifulSoup
from django.shortcuts import get_object_or_404
import markdown
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site

import os, sys
opencyb_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(opencyb_dir)

from articles import models as articles_models
from news import models as news_models
from projects import models as projects_models

from articles import views as articles_views

register = template.Library()

@register.filter
def preview(value):
    return "".join(value.split('\n')[:3])

@register.filter
def html_edit(value):
    soup = BeautifulSoup(value, "html.parser")
    
    # Add id to image (for open by click)
    for img in soup.find_all('img'):
        # img['class'] = 'popup-image'
        link = img['src']
        a_tag = soup.new_tag('a')
        a_tag['href'] = link
        a_tag['class'] = 'fancylight popup-btn'
        a_tag['data-fancybox-group'] = 'light'

        img_tag = soup.new_tag('img')
        img_tag['class'] = 'lazy img-fluid'
        img_tag['alt'] = ""
        img_tag['data-src'] = link
        
        a_tag.append(img_tag)
        img.parent.append(a_tag)
        img.extract()
    
    # Replace all youtube-link to iframe video integrated to html code
    for a in soup.find_all(text="youtube-link"):
        link = a.parent['href']

        div_video_tag = soup.new_tag('div')
        div_video_tag['class'] = 'youtube-video' # Add class for add styles in .css
        div_video_tag['style'] = "position: relative; width: 100%; height: 0; padding-bottom: 56.25%;"

        iframe_tag = soup.new_tag('iframe')
        iframe_tag['src'] = link
        iframe_tag['frameborder'] = '0'
        # iframe_tag['allow'] = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture'
        iframe_tag['allowfullscreen'] = None
        iframe_tag['class'] = 'youtube-video-type1'
        iframe_tag['style'] = "position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
        

        div_video_tag.append(iframe_tag)
        a.parent.parent.append(div_video_tag)

        a.parent.extract() # Remove <a> with href (custom markdown style)
    

    for link in soup.find_all('a', href=True):
        link['target'] = '_blank'


    for a in soup.find_all(text="code-snippet"):
        link = a.parent['href']

        div_snippet_tag = soup.new_tag('div')
        div_snippet_tag['class'] = 'code-snippet'
        div_snippet_tag['style'] = 'margin-bottom: 15px;'

        from snippets import models as snippets_models
        snippet_slug = link.rstrip('/').split('/')[-1]
        snippet = get_object_or_404(snippets_models.Snippet, slug=snippet_slug)
        
        from pygments import highlight
        from pygments.lexers import get_lexer_by_name
        from pygments.formatters import HtmlFormatter
        lexer = get_lexer_by_name(str(snippet.language).lower(), stripall=True)
        formatter = HtmlFormatter(linenos=True, cssclass='codehilite')
        result = highlight(snippet.code, lexer, formatter)

        snippet_share_tag = soup.new_tag('a')
        snippet_share_tag['class'] = 'card-text text-muted h6 float-left mt-0'
        snippet_share_tag['id'] = snippet_slug
        snippet_share_tag['href'] = link
        snippet_share_tag['target'] = '_blank'
        snippet_share_tag['style'] = 'position: absolute; right: 0; margin-right: 5%;'
        snippet_share_tag.append('????????????????????')

        div_snippet_tag.append(BeautifulSoup(result, 'html.parser'))
        div_snippet_tag.append(snippet_share_tag)
        div_snippet_tag.append(BeautifulSoup('<br>', 'html.parser'))
        a.parent.parent.append(div_snippet_tag)
        a.parent.extract()
        
    
    html_content = str(soup)
    
    return html_content

@register.filter
def custom_markdown(value):
    md_text = value
    html = markdown.markdown(md_text, extensions=['fenced_code', 'codehilite', 'tables'])
    return html

@register.inclusion_tag('recent/recent_articles.html')
def render_recent_articles():
    recent_articles_list = articles_models.Article.objects.filter(status=1)[:3]
    
    return {
        'articles_list': recent_articles_list
    }

@register.inclusion_tag('recent/recent_news.html')
def render_recent_news():
    recent_news_list = news_models.New.objects.all().filter(status=1)[:3]
    
    return {
        'news_list': recent_news_list
    }

@register.inclusion_tag('recent/recent_projects.html')
def render_recent_projects():
    recent_projects_list = projects_models.Project.objects.all().filter(status=1)[:3]
    
    return {
        'projects_list': recent_projects_list
    }

@register.inclusion_tag('recent/recent_comments.html', takes_context=True)
def render_recent_comments(context):
    domain = context['request'].headers['Host']
    template_url = 'http://{}/{}/{}/#comment-{}'

    recent_articles_comments = articles_models.Comment.objects.all().filter(active=True)
    recent_news_comments = news_models.Comment.objects.all().filter(active=True)
    recent_projects_comments = projects_models.Comment.objects.all().filter(active=True)
    recent_comments = []

    max_title_length = 100
    for i in recent_articles_comments: # i.article.slug
        recent_comments.append([i.created_on, i.name, template_url.format(domain, 'articles', i.article.slug, i.id), '%s..'%i.article.title[:max_title_length] if len(i.article.title) > max_title_length else i.article.title, i.website, i.id])
    
    for i in recent_news_comments:
        recent_comments.append([i.created_on, i.name, template_url.format(domain, 'news', i.new.slug, i.id), '%s..'%i.new.title[:max_title_length] if len(i.new.title) > max_title_length else i.new.title, i.website, i.id])
    
    for i in recent_projects_comments:
        recent_comments.append([i.created_on, i.name, template_url.format(domain, 'projects', i.project.slug, i.id), '%s..'%i.project.title[:max_title_length] if len(i.project.title) > max_title_length else i.project.title, i.website, i.id])
    
    recent_comments = sorted(recent_comments, key=lambda x: x[0], reverse = True)[:4]

    return {
        'comments_list': recent_comments
    }