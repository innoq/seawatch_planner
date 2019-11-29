from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class Skill(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True)
    SKILL_GROUPS = [
        ('lang', 'language'),
        ('other', 'other')
    ]
    group = models.CharField(max_length=10, choices=SKILL_GROUPS)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    citizenship = models.CharField(max_length=100)
    second_citizenship = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=100)
    country_of_birth = models.CharField(max_length=100)
    GENDER_CHOICES = [
        ('f', 'female'),
        ('m', 'male'),
        ('d', 'diverse')
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.CharField(max_length=200, blank=True)
    needs_schengen_visa = models.BooleanField()
    phone = models.CharField(max_length=100)
    emergency_contact = models.TextField(blank=True)
    comments = models.TextField(blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    custom_skills = models.CharField(max_length=500, blank=True)
    requested_positions = models.ManyToManyField(Position, related_name='requested_profiles')
    approved_positions = models.ManyToManyField(Position, related_name='approved_profiles', blank=True)

    def __str__(self):
        return self.last_name + ", " + self.first_name


class DocumentType(models.Model):
    name = models.CharField(max_length=100)
    DOCUMENT_TYPE_GROUPS = [
        ('ident', 'identification documents and visa'),
        ('nautic', 'nautical qualification'),
        ('engineer', 'engineer qualification'),
        ('seafarer', 'seafarer qualification'),
        ('other', 'other qualification')
    ]
    group = models.CharField(max_length=10, choices=DOCUMENT_TYPE_GROUPS)

    def __str__(self):
        return self.name


class Document(models.Model):
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    number = models.CharField(max_length=100, blank=True)
    issuing_date = models.DateField(blank=True)
    expiry_date = models.DateField(blank=True)
    issuing_authority = models.CharField(max_length=100, blank=True)
    issuing_place = models.CharField(max_length=100, blank=True)
    issuing_country = models.CharField(max_length=100, blank=True)
    file = models.FileField()

    def __str__(self):
        return f'{self.number} ({self.document_type})'


class Question(models.Model):
    text = models.CharField(max_length=500)
    mandatory = models.BooleanField()
    profiles = models.ManyToManyField(Profile, through='Answer')

    def __str__(self):
        return self.text


class Answer(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text


class Availability(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.start_date.strftime("%x")} – {self.start_date.strftime("%x")} ({self.profile})'

    def clean(self):
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError({
                    'start_date': ValidationError(_('Start Date has to be before End Date.')),
                    'end_date': ValidationError(_('End Date has to be after Start Date.')),
                })
