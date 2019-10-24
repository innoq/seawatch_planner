from django.db import models

# Create your models here.
class Ship(models.Model):
    name = models.CharField(max_length=30)

class Mission(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE)

