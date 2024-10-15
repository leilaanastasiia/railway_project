from django import forms
from railway.models import Route


class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['name', 'description']