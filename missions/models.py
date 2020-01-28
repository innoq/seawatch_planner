from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import FieldTracker

from seawatch_registration.models import Position


# Create your models here.
class Ship(models.Model):
    name = models.CharField(max_length=30, verbose_name=_('Name'))

    def __str__(self):
        return self.name


class Mission(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    start_date = models.DateField(verbose_name=_('Start date'))
    end_date = models.DateField(verbose_name=_('End date'))
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE, verbose_name=_('Ship'))

    def __str__(self):
        return self.ship.name + ": " + self.name

    def get_assigned_users(self):
        return User.objects.filter(assignments__mission=self).distinct()


class Assignment(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, verbose_name=_('Mission'))
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name=_('Position'))
    user = models.ForeignKey(User,
                             on_delete=models.PROTECT,
                             default=None,
                             blank=True,
                             null=True,
                             related_name='assignments',)
    confirmed = models.BooleanField(default=False, verbose_name=_('Confirmed'))
    email_sent = models.BooleanField(default=False, verbose_name=_('Email sent'))

    tracker = FieldTracker(fields=['user'])


class DefaultAssignment(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name=_('Position'))
    quantity = models.IntegerField(verbose_name=_('Quantity'))
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE, related_name='default_assignments', verbose_name=_('Ship'))

    def clean(self):
        if self.quantity:
            if self.quantity < 1:
                raise ValidationError({
                    'quantity': ValidationError(_('Quantity must be at least one.'))
                })

    class Meta:
        unique_together = ('position', 'ship')
