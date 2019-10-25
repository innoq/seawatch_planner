from django.contrib import admin
from .models import Profile, Position, ProfilePosition, DocumentType, Document, Skill, Question, Answer

admin.site.register(Profile)
admin.site.register(Position)
admin.site.register(ProfilePosition)
admin.site.register(DocumentType)
admin.site.register(Document)
admin.site.register(Skill)
admin.site.register(Question)
admin.site.register(Answer)
