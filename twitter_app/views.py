from django.shortcuts import render
from django.views import generic


def index(request):
    template_name = 'twitter_app/index.html'
    return render(request, template_name)

