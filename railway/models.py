from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class RailwayStation(models.Model):
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return f'{self.name}'


class Train(models.Model):
    class Type(models.TextChoices):
        CARGO = 'CT', _('Cargo Train')
        PASSENGER = 'PT', _('Passenger Train')

    number = models.CharField(max_length=6, blank=False)
    type = models.CharField(max_length=2, choices=Type.choices, default=Type.PASSENGER, blank=False)

    def __str__(self):
        return f'{self.number}, {self.type}'


class Route(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField()

    def clean(self):
        if not self.name:  # does not have an effect until more complex validation
            raise ValidationError(_('Name is required'))
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'