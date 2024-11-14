from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Subquery, OuterRef
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView

from railway.forms import TicketForm
from railway.models import Ticket, RailwayStation, Route, Train, RouteStation


class TicketSearchView(LoginRequiredMixin, TemplateView):
    template_name = 'railway/tickets/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_station_id = self.request.GET.get('start_station')
        end_station_id = self.request.GET.get('end_station')
        stations = RailwayStation.objects.all()

        if start_station_id and end_station_id:
            start_station = RailwayStation.objects.get(id=start_station_id)
            end_station = RailwayStation.objects.get(id=end_station_id)
            routes = Route.objects.filter(
                routestation__station=start_station,
                routestation__order__lt=Subquery(
                    RouteStation.objects.filter(
                        route=OuterRef('pk'),
                        station=end_station
                    ).values('order')[:1]  # limiting the subquery to a single row
                )
            )
            trains = Train.objects.filter(
                route__in=routes,
                type=Train.Type.PASSENGER)
            context.update({
                'stations': stations,
                'routes': routes,
                'start_station': start_station,
                'end_station': end_station,
                'trains': trains
            })
        else:
            context['stations'] = stations

        return context

class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    template_name = 'railway/generic/form.html'
    form_class = TicketForm
    success_url = reverse_lazy('railway:ticket_search')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'Ticket'
        context['action'] = 'Buy'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['start'] = self.kwargs.get('start')
        kwargs['end'] = self.kwargs.get('end')
        kwargs['train'] =  self.kwargs.get('train')
        return kwargs
