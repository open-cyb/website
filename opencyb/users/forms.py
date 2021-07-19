# Third party imports
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Local application import
from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    image = forms.URLField(widget=forms.URLInput(
        attrs={'class': 'form-contro', 'placeholder': 'Ссылка на картинку', 'style': 'margin-bottom: 15px;'}
    ))
    phone_number = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Телефон..', 'style':'margin-bottom:15px;'}
    ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email..', 'style':'margin-bottom:15px;'}
    ))
    links_json = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': '6', 'placeholder': 'Ссылка в json формате..', 'style':'margin-bottom:15px;'}
    ))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': '10', 'placeholder': 'Описание, род деятельности и т.д.', 'style':'margin-bottom:15px;'}
    ))

    class Meta:
        model = Profile

        fields = ('image', 'phone_number', 'email', 'links_json', 'description')