from django import forms
from railway.models import Route, RailwayStation, Train


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