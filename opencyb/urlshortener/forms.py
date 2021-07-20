from django import forms
from .models import Shortener
from django.contrib.auth.models import User

class ShortenerForm(forms.ModelForm):
    long_url = forms.URLField(widget=forms.URLInput(
        attrs={"class": "form-control form-control-lg", "placeholder": "Ваш URL для сокращения", "style": "margin-bottom:15px;"}
    ))
    author = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control', 'style':'margin-bottom:15px;'}
    ))

    class Meta:
        model = Shortener

        fields = ('long_url', 'author')