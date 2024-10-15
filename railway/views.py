from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from railway.forms import RouteForm
from railway.models import RailwayStation, Train, Route


class RouteListView(ListView):
    model = Route
    template_name = 'railway/routes.html'
    context_object_name = 'routes'
    paginate_by = 10


class RouteDetailView(DetailView):
    model = Route
    template_name = 'railway/route_detail.html'
    context_object_name = 'route'


class RouteCreateView(CreateView):
    model = Route
    template_name = 'railway/route_create.html'
    form_class = RouteForm
    success_url = reverse_lazy('railway:routes')


class RouteUpdateView(UpdateView):
    model = Route
    form_class = RouteForm
    template_name = 'railway/route_update.html'
    success_url = reverse_lazy('railway:routes')


class RouteDeleteView(DeleteView):
    model = Route
    template_name = 'railway/route_delete.html'
    success_url = reverse_lazy('railway:routes')
