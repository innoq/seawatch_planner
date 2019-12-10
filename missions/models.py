from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

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


class DefaultAssignment(models.Model):
    position = models.ForeignKey(Position, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE, related_name='default_assignments')

    def clean(self):
        if self.quantity:
            if self.quantity < 1:
                raise ValidationError({
                    'quantity': ValidationError('Quantity must be at least one.')
                })
