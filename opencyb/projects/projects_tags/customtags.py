from django import template

register = template.Library()

@register.filter
def preview(value):
    return "".join(value.split('\n')[:3])