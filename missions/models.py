from django.contrib.auth.models import User
from django.db import models

from seawatch_registration.models import Position


# Create your models here.
class Ship(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        permissions = (('can_create_ships', 'Create ships'),
                       ('can_view_ships', 'View ships'),
                       ('can_update_ships', 'Update ships'),
                       ('can_delete_ships', 'Delete ships'))


class Mission(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE)

    def __str__(self):
        return self.ship.name + ": " + self.name

    class Meta:
        permissions = (('can_create_missions', 'Create missions'),
                       ('can_view_missions', 'View missions'),
                       ('can_update_missions', 'Update missions'),
                       ('can_delete_missions', 'Delete missions'))


class Assignment(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.PROTECT)
    user = models.ForeignKey(User,
                             on_delete=models.PROTECT,
                             default=None,
                             blank=True,
                             null=True,
                             related_name='assignments')

    class Meta:
        permissions = (('can_create_assignment', 'Create assignments'),
                       ('can_view_assignment', 'View assignments'),
                       ('can_update_assignment', 'Update assignments'),
                       ('can_delete_assignment', 'Delete assignments'))

