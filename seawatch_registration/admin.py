from django.contrib import admin

from .models import (Answer, Availability, Document, DocumentType, Position,
                     Profile, Question, Skill)

admin.site.register(Profile)
admin.site.register(Position)
admin.site.register(DocumentType)
admin.site.register(Document)
admin.site.register(Skill)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Availability)
