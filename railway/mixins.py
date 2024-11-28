from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render

from railway.forms import CoupeWagonForm, SVWagonForm, PlatzWagonForm, SittingWagonForm, TankWagonForm
from railway.models import CustomUser, CoupeWagon, PlatzWagon, SVWagon, SittingWagon, TankWagon


class IsAdminUserMixin(UserPassesTestMixin):
    permission_denied_message = 'Sorry, an access is limited to the stuff only.'

    def test_func(self):
        return self.request.user.type == CustomUser.Type.ADMIN

    def get_permission_denied_message(self):
        return self.permission_denied_message

    def handle_no_permission(self):
        return render(
            self.request,
            'railway/access_denied.html',
            {'message': self.get_permission_denied_message(),}
        )


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