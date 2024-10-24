from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView

from railway.forms import CoupeWagonForm, SVWagonForm, PlatzWagonForm, SittingWagonForm, TankWagonForm
from railway.models import CoupeWagon, PlatzWagon, SVWagon, SittingWagon, TankWagon


class WagonTypesView(TemplateView):
    template_name = 'railway/wagons/all_wagons_types.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'pass_types': ['Coupe', 'SV', 'Platz', 'Sitting'],
            'cargo_types': ['Tank'],
        })
        return context

class WagonTypeMixin:
    def get_model(self):
        wagon_type = self.kwargs.get('type').lower()
        if wagon_type == 'coupe':
            return CoupeWagon
        elif wagon_type == 'platz':
            return PlatzWagon
        elif wagon_type == 'sv':
            return SVWagon
        elif wagon_type == 'sitting':
            return SittingWagon
        elif wagon_type == 'tank':
            return TankWagon
        return None

    def get_form_class(self):
        wagon_type = self.kwargs.get('type').lower()
        if wagon_type == 'coupe':
            return CoupeWagonForm
        elif wagon_type == 'platz':
            return PlatzWagonForm
        elif wagon_type == 'sv':
            return SVWagonForm
        elif wagon_type == 'sitting':
            return SittingWagonForm
        elif wagon_type == 'tank':
            return TankWagonForm
        return None

class WagonListView(WagonTypeMixin, ListView):
    template_name = 'railway/generic/list.html'
    context_object_name = 'objects'
    paginate_by = 10

    def get_queryset(self):
        model = self.get_model()
        return model.objects.all() if model else []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wagon_type = self.kwargs.get('type')
        context.update({
            'page_title': f'{wagon_type.capitalize()} wagons',
            'list_title': f'List of {wagon_type} wagons:',
            'add_button_text': f'Add {wagon_type} wagon',
            'add_url_name': 'railway:wagon_create',
            'detail_url_name': 'railway:wagon_detail',
            'empty_message': f'No {wagon_type} wagons available.',
            'type': wagon_type,
        })
        return context

class WagonDetailView(WagonTypeMixin, DetailView):
    template_name = 'railway/wagons/wagon_detail.html'
    context_object_name = 'wagon'

    def get_object(self, queryset=None):
        model = self.get_model()
        return model.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wagon_type = self.kwargs.get('type')
        context.update({
            'type': wagon_type,
            'update_url_name': 'railway:wagon_update',
            'delete_url_name': 'railway:wagon_delete',
        })
        return context


class WagonCreateView(WagonTypeMixin, CreateView):
    template_name = 'railway/generic/form.html'
    
    def get_form_class(self):
        return super().get_form_class()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wagon_type = self.kwargs.get('type')
        context['object_name'] = f'{wagon_type} wagon'
        context['action'] = 'Create'
        return context

    def get_success_url(self):
        return reverse_lazy('railway:wagon_list', kwargs={'type': self.kwargs.get('type')})


class WagonUpdateView(WagonTypeMixin, UpdateView):
    template_name = 'railway/generic/form.html'

    def get_form_class(self):
        return super().get_form_class()

    def get_object(self, queryset=None):
        model = self.get_model()
        return model.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wagon_type = self.kwargs.get('type')
        context['object_name'] = f'{wagon_type} wagon'
        context['action'] = 'Update'
        return context

    def get_success_url(self):
        return reverse_lazy('railway:wagon_detail', kwargs={'type': self.kwargs.get('type'), 'pk': self.object.pk})


class WagonDeleteView(WagonTypeMixin, DeleteView):
    template_name = 'railway/generic/delete.html'

    def get_object(self, queryset=None):
        model = self.get_model()
        return model.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wagon_type = self.kwargs.get('type')
        context['object_name'] = f'{wagon_type} wagon'
        return context

    def get_success_url(self):
        return reverse_lazy('railway:wagon_list', kwargs={'type': self.kwargs.get('type')})

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
