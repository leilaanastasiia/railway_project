from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from railway.forms import RouteForm, StationForm, TrainForm
from railway.models import RailwayStation, Train, Route


class RouteListView(ListView):
    model = Route
    template_name = 'railway/routes/routes.html'
    context_object_name = 'routes'
    paginate_by = 10


class RouteDetailView(DetailView):
    model = Route
    template_name = 'railway/routes/route_detail.html'
    context_object_name = 'route'


class RouteCreateView(CreateView):
    model = Route
    template_name = 'railway/routes/route_create.html'
    form_class = RouteForm
    success_url = reverse_lazy('railway:routes')


class RouteUpdateView(UpdateView):
    model = Route
    form_class = RouteForm
    template_name = 'railway/routes/route_update.html'
    success_url = reverse_lazy('railway:routes')


class RouteDeleteView(DeleteView):
    model = Route
    template_name = 'railway/routes/route_delete.html'
    success_url = reverse_lazy('railway:routes')


class StationListView(ListView):
    model = RailwayStation
    template_name = 'railway/stations/stations.html'
    context_object_name = 'stations'
    paginate_by = 10


class StationDetailView(DetailView):
    model = RailwayStation
    template_name = 'railway/stations/stations_detail.html'
    context_object_name = 'station'


class StationCreateView(CreateView):
    model = RailwayStation
    template_name = 'railway/stations/station_create.html'
    form_class = StationForm
    success_url = reverse_lazy('railway:stations')


class StationUpdateView(UpdateView):
    model = RailwayStation
    form_class = StationForm
    template_name = 'railway/stations/station_update.html'
    success_url = reverse_lazy('railway:stations')


class StationDeleteView(DeleteView):
    model = RailwayStation
    template_name = 'railway/stations/station_delete.html'
    context_object_name = 'station'
    success_url = reverse_lazy('railway:stations')


class TrainListView(ListView):
    model = Train
    template_name = 'railway/trains/trains.html'
    context_object_name = 'trains'
    paginate_by = 10


class TrainDetailView(DetailView):
    model = Train
    template_name = 'railway/trains/train_detail.html'
    context_object_name = 'train'


class TrainCreateView(CreateView):
    model = Train
    template_name = 'railway/trains/train_create.html'
    form_class = TrainForm
    success_url = reverse_lazy('railway:trains')


class TrainUpdateView(UpdateView):
    model = Train
    form_class = TrainForm
    template_name = 'railway/trains/train_update.html'
    success_url = reverse_lazy('railway:trains')


class TrainDeleteView(DeleteView):
    model = Train
    template_name = 'railway/trains/train_delete.html'
    context_object_name = 'train'
    success_url = reverse_lazy('railway:trains')