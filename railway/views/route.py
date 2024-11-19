from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from railway.forms import RouteForm, RouteStationFormSet
from railway.models import Route, RouteStation


class RouteListView(LoginRequiredMixin, ListView):
    model = Route
    template_name = 'railway/generic/list.html'
    context_object_name = 'objects'
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Routes',
            'add_url_name': 'railway:route_create',
            'detail_url_name': 'railway:route',
            'object_name': 'Route',
            'empty_message': 'No routes yet.',
            'list_title': "Route's list:",
            'add_button_text': 'Add route'
        })
        return context


class RouteDetailView(LoginRequiredMixin, DetailView):
    model = Route
    template_name = 'railway/routes/route_detail.html'


class RouteCreateView(LoginRequiredMixin, CreateView):
    model = Route
    template_name = 'railway/generic/form.html'
    form_class = RouteForm
    success_url = reverse_lazy('railway:routes')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'Route'
        context['action'] = 'Create'
        return context


class RouteUpdateView(LoginRequiredMixin, UpdateView):
    model = Route
    form_class = RouteForm
    template_name = 'railway/generic/form.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'Route'
        context['action'] = 'Update'
        return context
    def get_success_url(self):
        return reverse_lazy('railway:route', kwargs={'pk': self.object.pk})


class RouteStationUpdateView(LoginRequiredMixin, View):
    template_name = 'railway/routes/routestation_update.html'
    def get(self, request, pk):
        route = get_object_or_404(Route, pk=pk)
        formset = RouteStationFormSet(
            queryset=RouteStation.objects.filter(route=route),
            form_kwargs={'route': route}
        )
        return render(request, self.template_name, {'formset': formset, 'route': route})
    def post(self, request, pk):
        route = get_object_or_404(Route, pk=pk)
        formset = RouteStationFormSet(
            request.POST,
            queryset=RouteStation.objects.filter(route=route),
            form_kwargs={'route': route}
        )
        if formset.is_valid():
            formset.save()
            return redirect('railway:route', pk=pk)
        return render(request, self.template_name, {'formset': formset, 'route': route})


class RouteDeleteView(LoginRequiredMixin, DeleteView):
    model = Route
    template_name = 'railway/generic/delete.html'
    success_url = reverse_lazy('railway:routes')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'route'
        return context
