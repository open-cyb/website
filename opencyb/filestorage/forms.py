from .models import File
from django import forms
from django.contrib.auth.models import User

class FileForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Название файла...', 'style':'margin-bottom:15px;'}
    ))
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}))
    author = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control', 'style':'margin-bottom:15px;'}
    ))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': '10', 'placeholder': 'Описание файла..', 'style':'margin-bottom:15px;'}
    ))

    class Meta:
        model = File

        fields = ('title', 'author', 'file', 'description')