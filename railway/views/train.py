from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from railway.forms import TrainForm, TrainRouteForm
from railway.models import Train


class TrainListView(ListView):
    model = Train
    template_name = 'railway/generic/list.html'
    context_object_name = 'objects'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Trains',
            'add_url_name': 'railway:train_create',
            'detail_url_name': 'railway:train',
            'object_name': 'Train',
            'empty_message': 'No trains yet.',
            'list_title': "Train's list:",
            'add_button_text': 'Add train'
        })
        return context


class TrainDetailView(DetailView):
    model = Train
    template_name = 'railway/trains/train_detail.html'
    context_object_name = 'train'


class TrainCreateView(CreateView):
    model = Train
    template_name = 'railway/generic/form.html'
    form_class = TrainForm
    success_url = reverse_lazy('railway:trains')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'Train'
        context['action'] = 'Create'
        return context


class TrainUpdateView(UpdateView):
    model = Train
    form_class = TrainForm
    template_name = 'railway/generic/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'Train'
        context['action'] = 'Update'
        return context

    def get_success_url(self):
        return reverse_lazy('railway:train', kwargs={'pk': self.object.pk})

class TrainAddRouteView(UpdateView):
    model = Train
    form_class = TrainRouteForm
    template_name = 'railway/generic/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'To The Train'
        context['action'] = 'Add Route'
        return context

    def get_success_url(self):
        return reverse_lazy('railway:train', kwargs={'pk': self.object.pk})


class TrainDeleteView(DeleteView):
    model = Train
    template_name = 'railway/generic/delete.html'
    context_object_name = 'train'
    success_url = reverse_lazy('railway:trains')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'train'
        return context
