from django.shortcuts import render, get_object_or_404
# from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile

def profiles_page(request):
    template_name = 'contacts.html'
    profiles = Profile.objects.all()

    return render(request, template_name, {'profiles': profiles})

def profile_detail(request, slug):
    template_name = 'profile_detail.html'
    profile = get_object_or_404(Profile, slug=slug)

    return render(request, template_name, {'profile': profile})