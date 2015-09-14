from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello user, this is my twitter app")
