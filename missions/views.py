from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from datetime import datetime

# Create your views here.


def index(request):
    template = loader.get_template('missions.html')
    context = {
        "greeting": "Hello"
    }
    return HttpResponse(template.render(context, request))


def show_mission_editor(request):
    template = loader.get_template('edit_mission.html')
    context = {
        "mission_id": "Mission 1",
        "start": datetime(2020, 1, 1),
        "end": datetime(2020, 1, 31),
        "ship": "Nautilus"
    }
    return HttpResponse(template.render(context, request))
