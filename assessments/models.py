from django.db import models

from seawatch_registration.models import Profile


class Assessment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    ASSESSMENT_STATUS = [
        ('pending', 'pending'),
        ('accepted', 'accepted'),
        ('rejected', 'rejected')
    ]
    status = models.CharField(max_length=10, choices=ASSESSMENT_STATUS)
    comment = models.TextField(blank=True)

    class Meta:
        permissions = (('can_assess_profiles', 'Set assessments for profiles'),)
