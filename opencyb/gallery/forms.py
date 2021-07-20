from .models import Photo
from django import forms

class PhotoForm(forms.ModelForm):
    photo = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}))

    class Meta:
        model = Photo

        fields = ('title', 'author', 'photo', 'description')