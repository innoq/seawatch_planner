from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {'home_nav_class': 'active'})
