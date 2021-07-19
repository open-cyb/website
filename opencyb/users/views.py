from django.shortcuts import render, get_object_or_404
from django.urls.resolvers import get_resolver
from .forms import ProfileUpdateForm
from .models import Profile
import json
from django.http import HttpResponseRedirect

def profiles_page(request):
    template_name = 'users/contacts.html'
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
    template_name = 'users/profile_detail.html'
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

def profile_edit(request, slug):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(request.build_absolute_uri('/'))
    
    template_name = 'users/profile_edit.html'
    context = {}
    edit_form = ProfileUpdateForm(instance = Profile.objects.get(slug=slug))
    context['form'] = edit_form

    if request.method == 'GET':
        return render(request, template_name, context)
    
    elif request.method == 'POST':
        instance = get_object_or_404(Profile, slug=slug)
        edit_form = ProfileUpdateForm(request.POST, instance=instance)

        if edit_form.is_valid():
            profile_object = edit_form.save()
            return HttpResponseRedirect(request.build_absolute_uri('/contacts/' + profile_object.slug))
        
        context['errors'] = edit_form.errors

        return render(request, template_name, context)