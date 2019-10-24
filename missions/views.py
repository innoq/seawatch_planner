from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.


def index(request):
    template = loader.get_template('missions.html')
    context = {
        "greeting": "Hello"
    }
    return HttpResponse(template.render(context, request))


def show_mission_editor(request):
    template = loader.get_template('edit_mission.html')
    context = { }
    return HttpResponse(template.render(context, request))
