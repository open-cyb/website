# Third party imports
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Local application import
from .models import Profile

# class UserUpdateForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('username')


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('slug', 'image', 'phone_number', 'email', 'links_json', 'description')