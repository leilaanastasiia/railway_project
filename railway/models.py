from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(unique=True, blank=False)

    def __str__(self):
        return f'id={self.id}, username={self.username}, email={self.email}'


class RailwayStation(models.Model):
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return f'{self.name}'


class Route(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=100, blank=False)
    description = models.TextField()
    stations = models.ManyToManyField(RailwayStation, related_name='routes', blank=True)

    def clean(self):
        if not self.name:  # does not have an effect until more complex validation
            raise ValidationError(_('Name is required'))
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

class Train(models.Model):
    class Type(models.TextChoices):
        CARGO = 'CT', _('Cargo Train')
        PASSENGER = 'PT', _('Passenger Train')

    number = models.CharField(max_length=6, blank=False)
    type = models.CharField(max_length=2, choices=Type.choices, default=Type.PASSENGER, blank=False)
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True, related_name='trains')
    station = models.ForeignKey(RailwayStation, on_delete=models.SET_NULL, null=True, blank=True, related_name='trains')

    def __str__(self):
        return f'{self.number}, {self.type}'


class Ticket(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    start_station = models.ForeignKey(RailwayStation, on_delete=models.CASCADE, related_name='departure_tickets')
    end_station = models.ForeignKey(RailwayStation, on_delete=models.CASCADE, related_name='arrival_tickets')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tickets')

    def __str__(self):
        return f'Ticket for {self.train.number} train from {self.start_station.name} to {self.end_station.name}'