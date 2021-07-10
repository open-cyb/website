from django import template
from bs4 import BeautifulSoup

register = template.Library()

@register.filter
def preview(value):
    return "".join(value.split('\n')[:3])

@register.filter
def html_edit(value):
    print(type(value))
    soup = BeautifulSoup(value)
    # Add id to image (for open by click)
    for img in soup.find_all('img'):
        img['class'] = 'popup-image'
    
    # Replace all youtube-link to iframe video integrated to html code
    for a in soup.find_all(text="youtube-link"):
        link = a.parent['href']
        a.parent.name='iframe'
        a.parent['src']=link
        a.parent['width']='70%'
        a.parent['height']='auto'
        #new_tag = soup.net_tag("iframe", src=link)
        #a.parent.parent.append(new_tag)
        #a.extract()
    
    html_content = str(soup)
    
    return html_content