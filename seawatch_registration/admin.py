from django.contrib import admin
from .models import Profile, Position, ProfilePosition

# Register your models here.
admin.site.register(Profile)
admin.site.register(Position)
admin.site.register(ProfilePosition)
