from django import forms
from .models import Shortener

class ShortenerForm(forms.ModelForm):
    long_url = forms.URLField(widget=forms.URLInput(
        attrs={"class": "form-control form-control-lg", "placeholder": "Ваш URL для сокращения"}
    ))

    class Meta:
        model = Shortener

        fields = ('long_url', )