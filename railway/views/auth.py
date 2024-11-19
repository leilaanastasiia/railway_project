from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from railway.forms import CustomUserRegistrationForm


class CustomUserRegistrationView(FormView):
    template_name = 'railway/registration/registration.html'
    form_class = CustomUserRegistrationForm
    success_url = reverse_lazy('railway:login')

# class CustomUserRegistrationView(TemplateView):
#     template_name = 'railway/registration/registration.html'
