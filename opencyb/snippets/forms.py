from django import forms
from .models import Snippet

class SnippetForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Название..', 'style':'margin-bottom:15px;'}
    ))
    language = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Язык..', 'style':'margin-bottom:15px;'}
    ))
    code = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': '10', 'placeholder': 'Code..', 'style':'margin-bottom:15px;'}
    ))

    class Meta:
        model = Snippet

        fields = ('title', 'language', 'code', )