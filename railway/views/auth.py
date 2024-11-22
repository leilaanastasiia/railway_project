from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django_registration.backends.activation.views import RegistrationView


class CustomRegistrationView(RegistrationView):
    success_url = reverse_lazy('railway:django_registration_complete')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_active:
            return redirect('railway:home')
        return super().dispatch(request, *args, **kwargs)
