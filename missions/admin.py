from django.contrib import admin

# Register your models here.
from .models import Assignment, DefaultAssignment, Mission, Ship


class AssignmentInline(admin.TabularInline):
    model = Assignment


class MissionAdmin(admin.ModelAdmin):
    inlines = [AssignmentInline]


admin.site.register(Ship)
admin.site.register(Mission, MissionAdmin)
admin.site.register(Assignment)
admin.site.register(DefaultAssignment)
