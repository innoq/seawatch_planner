from django.contrib import admin

from .models import (Answer, Availability, Document, DocumentType, Profile)

admin.site.register(Profile)
admin.site.register(DocumentType)
admin.site.register(Document)
admin.site.register(Answer)
admin.site.register(Availability)

