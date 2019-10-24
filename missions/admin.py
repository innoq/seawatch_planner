from django.contrib import admin

# Register your models here.
from .models import Ship, Mission

admin.site.register(Ship)
admin.site.register(Mission)