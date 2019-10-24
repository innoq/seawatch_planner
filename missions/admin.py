from django.contrib import admin

# Register your models here.
from .models import Ship, Mission, Assignment

class AssignmentInline(admin.TabularInline):
    model = Assignment

class MissionAdmin(admin.ModelAdmin):
    inlines = [AssignmentInline]

admin.site.register(Ship)
admin.site.register(Mission, MissionAdmin)
admin.site.register(Assignment)