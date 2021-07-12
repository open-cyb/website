from .models import Comment
from django import forms

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