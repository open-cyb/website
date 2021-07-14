from django.shortcuts import render, get_object_or_404
# from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile
import json

def profiles_page(request):
    template_name = 'contacts.html'
    profiles = Profile.objects.all()

    context = {}

    profiles_with_context = []

    for profile in list(profiles):
        links_json = None
        profile_context = {}
        if profile.links_json:
            links_json = json.loads(profile.links_json)
            for key, value in links_json.items():
                if key == 'vk':
                    profile_context['link_vk'] = value
                elif key == 'telegram':
                    profile_context['link_telegram'] = value
        profiles_with_context.append({'profile':profile, 'links': profile_context})
    
    # context['profiles'] = profiles
    context['profiles'] = profiles_with_context

    return render(request, template_name, context)

def profile_detail(request, slug):
    template_name = 'profile_detail.html'
    profile = get_object_or_404(Profile, slug=slug)
    links_json = None
    context = {}
    if profile.links_json:
        links_json = json.loads(profile.links_json)
        for key, value in links_json.items():
            if key == 'vk':
                context['link_vk'] = value
            elif key == 'telegram':
                context['link_telegram'] = value

    context['profile'] = profile

    return render(request, template_name, context)