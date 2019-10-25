from django.db import models
from django.contrib.auth.models import User

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
  email = models.CharField(max_length=100)
  needs_schengen_visa = models.BooleanField()
  phone = models.CharField(max_length=100)
  emergency_contact = models.TextField(blank=True)
  comments = models.TextField(blank=True)
  skills = models.ManyToManyField(Skill)
  custom_skills = models.CharField(max_length=500, blank=True)

  def __str__(self):
    return self.last_name + ", " + self.first_name

class Position(models.Model):
  name = models.CharField(max_length=100)
  profiles = models.ManyToManyField(Profile, through='ProfilePosition')

  def __str__(self):
    return self.name

class ProfilePosition(models.Model):
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
  position = models.ForeignKey(Position, on_delete=models.CASCADE)
  requested = models.BooleanField()
  approved = models.BooleanField()

  def __str__(self):
    return self.profile.__str__() + "-" + self.position.__str__()

class DocumentType(models.Model):
  name = models.CharField(max_length=100)
  DOCUMENT_TYPE_GROUPS=[
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
  file = models.BinaryField()

  def __str__(self):
    return f'{self.number} ({self.document_type})'
