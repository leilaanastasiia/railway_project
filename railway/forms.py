from django import forms
from django.forms import modelformset_factory

from railway.models import Route, RailwayStation, Train, CoupeWagon, PlatzWagon, SVWagon, SittingWagon, TankWagon, \
    RouteStation


class RouteStationForm(forms.ModelForm):
    class Meta:
        model = RouteStation
        fields = ['station', 'order', 'arrival_time', 'departure_time']
        

class BaseRouteStationFormSet(forms.BaseModelFormSet):
    def __init__(self, *args, route=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.route = route

    def _construct_form(self, i, **kwargs):
        form = super()._construct_form(i, **kwargs)
        form.instance.route = self.route
        return form


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


RouteStationFormSet = modelformset_factory(
    RouteStation,
    form=RouteStationForm,
    formset=BaseRouteStationFormSet,
    extra=2,
    can_delete=True,
)
