from django.contrib.auth.models import User
from django.db import models
from model_utils import FieldTracker

from seawatch_registration.models import Position


# Create your models here.
class Ship(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Mission(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE)

    def __str__(self):
        return self.ship.name + ": " + self.name


class Assignment(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.PROTECT)
    user = models.ForeignKey(User,
                             on_delete=models.PROTECT,
                             default=None,
                             blank=True,
                             null=True,
                             related_name='assignments')
    confirmed = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)

    tracker = FieldTracker(fields=['user'])
