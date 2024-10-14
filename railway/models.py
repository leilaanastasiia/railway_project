from django.db import models
from django.utils.translation import gettext_lazy as _


class RailwayStation(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class Train(models.Model):
    class Type(models.TextChoices):
        CARGO = 'CT', _('Cargo Train')
        PASSENGER = 'PT', _('Passenger Train')

    number = models.CharField(max_length=6)
    type = models.CharField(max_length=2, choices=Type.choices, default=Type.PASSENGER)

    def __str__(self):
        return f'{self.number}, {self.type}'