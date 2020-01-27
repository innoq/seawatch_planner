from django.db import models
from django.utils.translation import gettext_lazy as _

from seawatch_registration.models import Profile


class Assessment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_('Profile'))
    ASSESSMENT_STATUS = [
        ('pending', 'pending'),
        ('accepted', 'accepted'),
        ('rejected', 'rejected')
    ]
    status = models.CharField(max_length=10, choices=ASSESSMENT_STATUS, verbose_name=_('Status'))
    comment = models.TextField(blank=True, verbose_name=_('Comment'))

    class Meta:
        permissions = (('can_assess_profiles', 'Set assessments for profiles'),)
