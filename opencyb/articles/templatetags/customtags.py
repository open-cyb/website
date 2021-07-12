from django import template
from bs4 import BeautifulSoup
import markdown

import os, sys
opencyb_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(opencyb_dir)
from articles import models as articles_models
from news import models as news_models
from projects import models as projects_models

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
    return {
        'articles_list': articles_models.Article.objects.all().order_by('created_on')[::-1][:3]
    }

@register.inclusion_tag('snippets/recent_news.html')
def render_recent_news():
    return {
        'news_list': news_models.New.objects.all().order_by('created_on')[::-1][:3]
    }

@register.inclusion_tag('snippets/recent_projects.html')
def render_recent_projects():
    return {
        'projects_list': projects_models.Project.objects.all().order_by('created_on')[::-1][:3]
    }