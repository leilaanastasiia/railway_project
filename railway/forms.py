from django import forms
from railway.models import Route, RailwayStation, Train, CoupeWagon, PlatzWagon, SVWagon, SittingWagon, TankWagon


class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['name', 'description', 'stations']


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