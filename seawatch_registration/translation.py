from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from modeltranslation.translator import TranslationOptions, translator

from seawatch_registration.models import Position, Question, Skill


class PositionTranslationOptions(TranslationOptions):
    fields = ('name',)


class PositionAdmin(TranslationAdmin):
    pass


class QuestionTranslationOptions(TranslationOptions):
    fields = ('text',)


class QuestionAdmin(TranslationAdmin):
    pass


class SkillTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)


class SkillAdmin(TranslationAdmin):
    pass

translator.register(Position, PositionTranslationOptions)
admin.site.register(Position, PositionAdmin)
translator.register(Question, QuestionTranslationOptions)
admin.site.register(Question, QuestionAdmin)
translator.register(Skill, SkillTranslationOptions)
admin.site.register(Skill, SkillAdmin)

