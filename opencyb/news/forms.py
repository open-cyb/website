from .models import New, Comment
from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_slug

class NewForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Название..', 'style':'margin-bottom:15px;'}
    ))
    slug = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Slug..', 'style':'margin-bottom:15px;'}
    ), validators=[validate_slug], required=False)
    author = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control', 'style':'margin-bottom:15px;'}
    ))
    content = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': '10', 'placeholder': 'Содержимое статьи..', 'style':'margin-bottom:15px;'}
    ))
    status = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'form-control', 'style':'margin-bottom:15px;'}
    ), choices=[ (0, "Draft"), (1, "Publish") ])
    
    class Meta:
        model = New

        fields = ('title', 'slug', 'author', 'content', 'status')

class CommentForm(forms.ModelForm):
    # name = forms.CharField(label="Имя", required=True)
    # email = forms.EmailField(label="Email", required=False)
    # body = forms.CharField(label="Текст", required=True)
    class Meta:
        model = Comment
        fields = ('name', 'email', 'website', 'body')
        requireds={'website':False}
        labels = {
            'name': 'Имя',
            'email': 'Email',
            'website': 'web-сайт',
            'body': 'Текст'
        }