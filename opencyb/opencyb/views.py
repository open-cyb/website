from django.shortcuts import render, redirect

def redirect_to_news(request):
    response = redirect('/news/')
    return response