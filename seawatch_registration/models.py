from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries import Countries
from django_countries.fields import CountryField

from seawatch_registration.countries import data


class Nationalities(Countries):
    override = ((d['code'], _(d['demonym'] or d['name'])) for d in data)


class Skill(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    description = models.CharField(max_length=500, blank=True, verbose_name=_('Description'))
    SKILL_GROUPS = [
        ('lang', _('language')),
        ('other', _('other'))
    ]
    group = models.CharField(max_length=10, choices=SKILL_GROUPS)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    citizenship = CountryField(countries=Nationalities, multiple=True, verbose_name=_('Citizenship'))
    date_of_birth = models.DateField(verbose_name=_('Date of birth'))
    place_of_birth = models.CharField(max_length=100, verbose_name=_('Place of birth'))
    country_of_birth = CountryField(verbose_name=_('Country of birth'))
    GENDER_CHOICES = [
        ('f', _('female')),
        ('m', _('male')),
        ('d', _('diverse'))
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name=_('Gender'))
    address = models.CharField(max_length=200, blank=True, verbose_name=_('Address'))
    needs_schengen_visa = models.BooleanField(verbose_name=_('Needs Schengen Visa'))
    phone = models.CharField(max_length=100, verbose_name=_('Phone'))
    emergency_contact = models.TextField(blank=True, verbose_name=_('Emergency contact'))
    comments = models.TextField(blank=True, verbose_name=_('Comments'))
    skills = models.ManyToManyField(Skill, verbose_name=_('Skills'))
    custom_skills = models.CharField(max_length=500, blank=True, verbose_name=_('Custom skills'))
    requested_positions = models.ManyToManyField(Position,
                                                 related_name='requested_profiles',
                                                 verbose_name=_('Requested Positions'))
    approved_positions = models.ManyToManyField(Position,
                                                related_name='approved_profiles',
                                                blank=True,
                                                verbose_name=_('Approved Positions'))

    def __str__(self):
        return self.user.last_name + ", " + self.user.first_name

    def get_joined_citizenship_list(self, delimiter=', '):
        return delimiter.join(c.name for c in self.citizenship)


class DocumentType(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    DOCUMENT_TYPE_GROUPS = [
        ('ident', _('identification documents and visa')),
        ('nautic', _('nautical qualification')),
        ('engineer', _('engineer qualification')),
        ('seafarer', _('seafarer qualification')),
        ('other', _('other qualification'))
    ]
    group = models.CharField(max_length=10, choices=DOCUMENT_TYPE_GROUPS, verbose_name=_('Category'))

    def __str__(self):
        return self.name


class Document(models.Model):
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE, verbose_name=_('Document type'))
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_('Profile'))
    number = models.CharField(max_length=100, blank=True, verbose_name=_('Number'))
    issuing_date = models.DateField(null=True, blank=True, verbose_name=_('Issuing date'))
    expiry_date = models.DateField(null=True, blank=True, verbose_name=_('Expiry date'))
    issuing_authority = models.CharField(max_length=100, blank=True, verbose_name=_('Issuing authority'))
    issuing_place = models.CharField(max_length=100, blank=True, verbose_name=_('Issuing place'))
    issuing_country = models.CharField(max_length=100, blank=True, verbose_name=_('Issuing country'))
    file = models.FileField(verbose_name=_('File'))

    def __str__(self):
        return f'{self.number} ({self.document_type})'


class Question(models.Model):
    text = models.CharField(max_length=500, verbose_name=_('Text'))
    mandatory = models.BooleanField(verbose_name=_('Madatory'))
    profiles = models.ManyToManyField(Profile, through='Answer', verbose_name=_('Profiles'))

    def __str__(self):
        return self.text


class Answer(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_('Profile'))
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=_('Question'))
    text = models.TextField(verbose_name=_('Text'))

    def __str__(self):
        return self.text


class Availability(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_('Profile'))
    start_date = models.DateField(verbose_name=_('Start date'))
    end_date = models.DateField(verbose_name=_('End date'))
    comment = models.CharField(max_length=255, blank=True, verbose_name=_('Comment'))

    def __str__(self):
        return f'{self.start_date.strftime("%x")} – {self.start_date.strftime("%x")} ({self.profile})'

    def clean(self):
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError({
                    'start_date': ValidationError(_('Cannot select an empty date range.')),
                    'end_date': ValidationError(_('Cannot select an empty date range.')),
                })
