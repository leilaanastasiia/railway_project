from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from railway.forms import StationForm
from railway.models import RailwayStation


class StationListView(LoginRequiredMixin, ListView):
    model = RailwayStation
    template_name = 'railway/generic/list.html'
    context_object_name = 'objects'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Stations',
            'add_url_name': 'railway:station_create',
            'detail_url_name': 'railway:station',
            'object_name': 'Station',
            'empty_message': 'No stations yet.',
            'list_title': "Station's list:",
            'add_button_text': 'Add station'
        })
        return context

class StationDetailView(LoginRequiredMixin, DetailView):
    model = RailwayStation
    template_name = 'railway/stations/stations_detail.html'


class StationCreateView(LoginRequiredMixin, CreateView):
    model = RailwayStation
    template_name = 'railway/generic/form.html'
    form_class = StationForm
    success_url = reverse_lazy('railway:stations')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'Station'
        context['action'] = 'Create'
        return context


class StationUpdateView(LoginRequiredMixin, UpdateView):
    model = RailwayStation
    form_class = StationForm
    template_name = 'railway/generic/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'Station'
        context['action'] = 'Update'
        return context

    def get_success_url(self):
        return reverse_lazy('railway:station', kwargs={'pk': self.object.pk})


class StationDeleteView(LoginRequiredMixin, DeleteView):
    model = RailwayStation
    template_name = 'railway/generic/delete.html'
    success_url = reverse_lazy('railway:stations')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'station'
        return context
