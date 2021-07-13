from django import template
from bs4 import BeautifulSoup
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
    soup = BeautifulSoup(value)
    # Add id to image (for open by click)
    for img in soup.find_all('img'):
        img['class'] = 'popup-image'
    
    # Replace all youtube-link to iframe video integrated to html code
    for a in soup.find_all(text="youtube-link"):
        link = a.parent['href']
        a.parent.name='iframe'
        a.parent['max-width']='100%'
        a.parent['height']='auto'
        a.parent['src']=link
        a.parent['title']='Youtube video player'
        a.parent['frameborder']='0'
        a.parent['allow']="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        a.parent['allowfullscreen']=None
        a.parent['class'] = 'youtube-video'
    
    html_content = str(soup)
    
    return html_content

@register.filter
def custom_markdown(value):
    md_text = value
    html = markdown.markdown(md_text, extensions=['fenced_code', 'codehilite'])
    
    return html

@register.inclusion_tag('snippets/recent_articles.html')
def render_recent_articles():
    recent_articles_list = articles_models.Article.objects.filter(status=1)[:3]
    
    return {
        'articles_list': recent_articles_list
    }

@register.inclusion_tag('snippets/recent_news.html')
def render_recent_news():
    recent_news_list = news_models.New.objects.all().filter(status=1)[:3]
    
    return {
        'news_list': recent_news_list
    }

@register.inclusion_tag('snippets/recent_projects.html')
def render_recent_projects():
    recent_projects_list = projects_models.Project.objects.all().filter(status=1)[:3]
    
    return {
        'projects_list': recent_projects_list
    }

@register.inclusion_tag('snippets/recent_comments.html', takes_context=True)
def render_recent_comments(context):
    domain = context['request'].headers['Host']
    template_url = 'http://{}/{}/{}/#comment-{}'

    recent_articles_comments = articles_models.Comment.objects.all().filter(active=True)
    recent_news_comments = news_models.Comment.objects.all().filter(active=True)
    recent_projects_comments = projects_models.Comment.objects.all().filter(active=True)
    recent_comments = []

    for i in recent_articles_comments: # i.article.slug
        recent_comments.append([i.created_on, i.name, template_url.format(domain, 'articles', i.article.slug, i.id), '%s..'%i.article.title[:32], i.website, i.id])
    
    for i in recent_news_comments:
        recent_comments.append([i.created_on, i.name, template_url.format(domain, 'news', i.new.slug, i.id), '%s..'%i.new.title[:32], i.website, i.id])
    
    for i in recent_projects_comments:
        recent_comments.append([i.created_on, i.name, template_url.format(domain, 'projects', i.project.slug, i.id), '%s..'%i.project.title[:32], i.website, i.id])
    
    recent_comments = sorted(recent_comments, key=lambda x: x[0], reverse = True)[:4]

    return {
        'comments_list': recent_comments
    }