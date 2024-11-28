from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from railway.validators import RouteStationValidator


class CustomUser(AbstractUser):

    class Type(models.TextChoices):
        ADMIN = 'Admin', _('Admin')
        CUSTOMER = 'Customer', _('Customer')

    type = models.CharField(max_length=8, choices=Type.choices, default=Type.CUSTOMER, blank=False)
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(unique=True, blank=False)

    def __str__(self):
        return f'id={self.id}, username={self.username}, email={self.email}'


class RailwayStation(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return f'{self.name}'


class Route(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)
    stations = models.ManyToManyField(RailwayStation, through='RouteStation', related_name='routes', blank=True)

    def get_stations(self):
        return self.routestation_set.all()

    def get_first_departure_time(self):
        route_stations = self.get_stations()
        if route_stations.exists():
            return route_stations.first().departure_time
        return None

    def get_last_arrival_time(self):
        route_stations = self.get_stations()
        if route_stations.count() > 1:
            return route_stations.last().arrival_time
        return None

    def get_total_travel_time(self):
        first_departure = self.get_first_departure_time()
        last_arrival = self.get_last_arrival_time()
        if first_departure and last_arrival:
            return last_arrival - first_departure
        return timedelta(0)

    def clean(self):
        if not self.name:  # does not have an effect until more complex validation
            raise ValidationError(_('Name is required'))
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'


class RouteStation(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    station = models.ForeignKey(RailwayStation, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(blank=False)
    arrival_time = models.DateTimeField(default=timezone.now, blank=False)
    departure_time = models.DateTimeField(default=timezone.now, blank=False)

    class Meta:
        ordering = ['order']

    def clean(self):
        validator = RouteStationValidator(self)
        validator.validate()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.full_clean()

    def __str__(self):
        return f'{self.station.name} on {self.route.name} (Position: {self.order})'


class Train(models.Model):
    class Meta:
        ordering = ["number"]

    class Type(models.TextChoices):
        CARGO = 'CT', _('Cargo Train')
        PASSENGER = 'PT', _('Passenger Train')

    number = models.CharField(max_length=6, blank=False)
    type = models.CharField(max_length=2, choices=Type.choices, default=Type.PASSENGER, blank=False)
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True, related_name='trains')
    station = models.ForeignKey(RailwayStation, on_delete=models.SET_NULL, null=True, blank=True, related_name='trains')
    reverse_sort_wagons = models.BooleanField(default=False)

    def get_wagons(self):
        all_wagons = []
        for related in self._meta.related_objects:
            if related.name.endswith('_wagons'):
                wagons = getattr(self, related.name).all()  # ex. train.coupewagon_wagons
                all_wagons.extend(wagons)
        return all_wagons

    def get_sorted_wagons(self):
        all_wagons = self.get_wagons()
        return sorted(all_wagons, key=lambda wagon: wagon.number, reverse=self.reverse_sort_wagons)

    def get_total_capacity(self):
        wagons = self.get_sorted_wagons()
        total_capacity = sum(wagon.capacity for wagon in wagons if hasattr(wagon, 'capacity'))
        return total_capacity

    def __str__(self):
        return f'{self.number}, {self.type}'


class Ticket(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='tickets')
    start_station = models.ForeignKey(RailwayStation, on_delete=models.CASCADE, related_name='departure_tickets')
    end_station = models.ForeignKey(RailwayStation, on_delete=models.CASCADE, related_name='arrival_tickets')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tickets')

    def __str__(self):
        return f'Ticket for {self.train.number} train from {self.start_station.name} to {self.end_station.name}'


class Wagon(models.Model):
    class Meta:
        abstract = True
        """
        unique among the train and (wagon_type)number, but not globally all numbers in the train 
        platz #1 and sv #1 still can exist inside one passenger train, 
        what is logically sufficient
        """
        constraints = [models.UniqueConstraint(fields=['train', 'number'], name='unique_%(class)s_number_per_train')]

    number = models.PositiveIntegerField(blank=True, validators=[MaxValueValidator(999999)])
    train = models.ForeignKey(Train, on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_wagons')

    def clean(self):
        if self.train and not self.is_valid_train_type():
            raise ValidationError(f"This wagon type can't be attached to {self.train.get_type_display()}. "
                                f"Expected train type: {'Passenger' if isinstance(self, PassengerWagon) else 'Cargo'}.")

    def is_valid_train_type(self):
        raise NotImplementedError("Subclasses must implement this method")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def get_classname(self):
        classname = self.__class__.__name__.lower()
        return classname.replace('wagon', '')


class PassengerWagon(Wagon):
    class Meta(Wagon.Meta):
        abstract = True

    def is_valid_train_type(self):
        return self.train.type == Train.Type.PASSENGER


class CargoWagon(Wagon):
    class Meta(Wagon.Meta):
        abstract = True

    def is_valid_train_type(self):
        return self.train.type == Train.Type.CARGO

class CoupeWagon(PassengerWagon):
    capacity = models.PositiveIntegerField(default=36, blank=False)

class PlatzWagon(PassengerWagon):
    capacity = models.PositiveIntegerField(default=54, blank=False)

class SVWagon(PassengerWagon):
    capacity = models.PositiveIntegerField(default=18, blank=False)

class SittingWagon(PassengerWagon):
    capacity = models.PositiveIntegerField(default=42, blank=False)

class TankWagon(CargoWagon):
    max_liters = models.FloatField(blank=False)
