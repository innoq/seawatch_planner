from django.contrib import admin
from .models import Profile, Position, ProfilePosition, DocumentType, Document

admin.site.register(Profile)
admin.site.register(Position)
admin.site.register(ProfilePosition)
admin.site.register(DocumentType)
admin.site.register(Document)
