from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  citizenship = models.CharField(max_length=100)
  second_citizenship = models.CharField(max_length=100)
  date_of_birth = models.DateField()
  place_of_birth = models.CharField(max_length=100)
  country_of_birth = models.CharField(max_length=100)
  GENDER_CHOICES = [
    ('f', 'female'),
    ('m', 'male'),
    ('d', 'diverse')
  ]
  gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
  address = models.CharField(max_length=200)
  email = models.CharField(max_length=100)
  needs_schengen_visa = models.BooleanField()
  phone = models.CharField(max_length=100)
  emergency_contact = models.TextField()
  comments = models.TextField()
