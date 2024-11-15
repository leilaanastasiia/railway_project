from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView

from railway.forms import CustomUserRegistrationForm


class CustomUserRegisterView(FormView):
    template_name = 'railway/registration/register.html'
    form_class = CustomUserRegistrationForm
    success_url = reverse_lazy('railway:login')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Succeeded.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, message=form.errors)
        return super().form_invalid(form)