from django.shortcuts import redirect
from django.urls import path, include, reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django_registration.backends.activation import views as django_registration_views

from railway.views import auth, index, route, station, train, wagon, ticket

app_name = 'railway'

urlpatterns = [
    path('home/', index.IndexView.as_view(), name='home'),
    path('', lambda request: redirect('home/', permanent=True)),

    #login & password management
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name='railway/registration/password_change.html',
            success_url=reverse_lazy('railway:password_change_done')),
        name='password_change'),
    path('password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(template_name='railway/registration/password_change_done.html'),
        name='password_change_done'),

    path('password_reset/',  # ask an email
        auth_views.PasswordResetView.as_view(
            success_url=reverse_lazy('railway:password_reset_done')),
        name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/',  # ask new password
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('railway:password_reset_complete')),
        name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # django-registration
    path('accounts/register/',  # 1) registration form
        auth.CustomRegistrationView.as_view(),
        name='django_registration_register'),
    path('accounts/register/complete/',  # 2) email has been sent & success massage
        TemplateView.as_view(template_name='railway/django_registration/registration_complete.html'),
        name='django_registration_complete'),
    path('accounts/activate/complete/',  # 4) successful activation message
        TemplateView.as_view(template_name='django_registration/activation_complete.html'),
        name='django_registration_activation_complete'),
    path('accounts/activate/',  # 3) link from the mail & activation_form with the key
        django_registration_views.ActivationView.as_view(success_url=reverse_lazy('railway:django_registration_activation_complete')),
        name='django_registration_activate'),

    # routes
    path('routes/', route.RouteListView.as_view(), name='routes'),
    path('routes/<int:pk>/', route.RouteDetailView.as_view(), name='route'),
    path('routes/add/', route.RouteCreateView.as_view(), name='route_create'),
    path('routes/<int:pk>/update/', route.RouteUpdateView.as_view(), name='route_update'),
    path('routes/<int:pk>/update_stations/', route.RouteStationUpdateView.as_view(), name='route_station_update'),
    path('routes/<int:pk>/delete/', route.RouteDeleteView.as_view(), name='route_delete'),

    #stations
    path('stations/', station.StationListView.as_view(), name='stations'),
    path('stations/<int:pk>/', station.StationDetailView.as_view(), name='station'),
    path('stations/add/', station.StationCreateView.as_view(), name='station_create'),
    path('stations/<int:pk>/update/', station.StationUpdateView.as_view(), name='station_update'),
    path('stations/<int:pk>/delete/', station.StationDeleteView.as_view(), name='station_delete'),

    #trains
    path('trains/', train.TrainListView.as_view(), name='trains'),
    path('trains/<int:pk>/', train.TrainDetailView.as_view(), name='train'),
    path('trains/add/', train.TrainCreateView.as_view(), name='train_create'),
    path('trains/<int:pk>/update/', train.TrainUpdateView.as_view(), name='train_update'),
    path('trains/<int:pk>/add_route/', train.TrainAddRouteView.as_view(), name='train_add_route'),
    path('trains/<int:pk>/delete/', train.TrainDeleteView.as_view(), name='train_delete'),

    #wagons
    path('wagons/types/', wagon.WagonTypesView.as_view(), name='wagon_types'),
    path('wagons/<str:type>/', wagon.WagonListView.as_view(), name='wagon_list'),
    path('wagons/<str:type>/create/', wagon.WagonCreateView.as_view(), name='wagon_create'),
    path('wagons/<str:type>/<int:pk>/', wagon.WagonDetailView.as_view(), name='wagon_detail'),
    path('wagons/<str:type>/<int:pk>/update/', wagon.WagonUpdateView.as_view(), name='wagon_update'),
    path('wagons/<str:type>/<int:pk>/delete/', wagon.WagonDeleteView.as_view(), name='wagon_delete'),

    #tickets
    path('tickets/search/', ticket.TicketSearchView.as_view(), name='ticket_search'),
    path('tickets/<int:pk>/', ticket.TicketDetailView.as_view(), name='ticket'),
    path('tickets/add/<int:start>/<int:end>/<int:train>', ticket.TicketCreateView.as_view(), name='ticket_add'),
]
