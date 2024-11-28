from django import forms
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory

from railway.models import Route, RailwayStation, Train, CoupeWagon, PlatzWagon, SVWagon, SittingWagon, TankWagon, \
    RouteStation, Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['user', 'start_station', 'end_station', 'train']


class TicketBuyForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = []

    def __init__(self, start, end, train, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.user = user
        self.instance.start_station = RailwayStation.objects.get(pk=start)
        self.instance.end_station = RailwayStation.objects.get(pk=end)
        self.instance.train = Train.objects.get(pk=train)


class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['name', 'description']


class StationForm(forms.ModelForm):
    class Meta:
        model = RailwayStation
        fields = ['name']


class TrainForm(forms.ModelForm):
    class Meta:
        model = Train
        fields = ['number', 'type', 'route', 'station']


class TrainRouteForm(forms.ModelForm):
    class Meta:
        model = Train
        fields = ['route']


class BasePassWagonForm(forms.ModelForm):
    class Meta:
        fields = ['number', 'train', 'capacity']


class BaseCargoWagonForm(forms.ModelForm):
    class Meta:
        fields = ['number', 'train']

class CoupeWagonForm(BasePassWagonForm):
    class Meta(BasePassWagonForm.Meta):
        model = CoupeWagon

class PlatzWagonForm(BasePassWagonForm):
    class Meta(BasePassWagonForm.Meta):
        model = PlatzWagon

class SVWagonForm(BasePassWagonForm):
    class Meta(BasePassWagonForm.Meta):
        model = SVWagon

class SittingWagonForm(BasePassWagonForm):
    class Meta(BasePassWagonForm.Meta):
        model = SittingWagon

class TankWagonForm(BaseCargoWagonForm):
    class Meta(BaseCargoWagonForm.Meta):
        model = TankWagon
        fields = BaseCargoWagonForm.Meta.fields + ['max_liters']


class RouteStationForm(forms.ModelForm):
    class Meta:
        model = RouteStation
        fields = ['station', 'order', 'arrival_time', 'departure_time']

    def __init__(self, route, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.route = route


RouteStationFormSet = modelformset_factory(
    RouteStation,
    form=RouteStationForm,
    extra=2,
    can_delete=True,
)
