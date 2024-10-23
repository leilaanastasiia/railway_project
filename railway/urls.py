from django.shortcuts import redirect
from django.urls import path

from railway.views.index import IndexView
from railway.views.route import RouteListView, RouteDetailView, RouteCreateView, RouteUpdateView, RouteDeleteView
from railway.views.station import StationListView, StationDetailView, StationCreateView, StationUpdateView, \
    StationDeleteView
from railway.views.train import TrainListView, TrainDetailView, TrainCreateView, TrainUpdateView, TrainDeleteView, \
    TrainAddRouteView
from railway.views.wagon import WagonTypesView, WagonListView, WagonCreateView, WagonUpdateView, WagonDeleteView, \
    WagonDetailView

app_name = 'railway'

urlpatterns = [
    path('home/', IndexView.as_view(), name='home'),
    path('', lambda request : redirect('home/', permanent=True)),

    # routes
    path('routes/', RouteListView.as_view(), name='routes'),
    path('routes/<int:pk>/', RouteDetailView.as_view(), name='route'),
    path('routes/add/', RouteCreateView.as_view(), name='route_create'),
    path('routes/<int:pk>/update/', RouteUpdateView.as_view(), name='route_update'),
    path('routes/<int:pk>/delete/', RouteDeleteView.as_view(), name='route_delete'),

    #stations
    path('stations/', StationListView.as_view(), name='stations'),
    path('stations/<int:pk>/', StationDetailView.as_view(), name='station'),
    path('stations/add/', StationCreateView.as_view(), name='station_create'),
    path('stations/<int:pk>/update/', StationUpdateView.as_view(), name='station_update'),
    path('stations/<int:pk>/delete/', StationDeleteView.as_view(), name='station_delete'),

    #trains
    path('trains/', TrainListView.as_view(), name='trains'),
    path('trains/<int:pk>/', TrainDetailView.as_view(), name='train'),
    path('trains/add/', TrainCreateView.as_view(), name='train_create'),
    path('trains/<int:pk>/update/', TrainUpdateView.as_view(), name='train_update'),
    path('trains/<int:pk>/add_route', TrainAddRouteView.as_view(), name='train_add_route'),
    path('trains/<int:pk>/delete/', TrainDeleteView.as_view(), name='train_delete'),

    #wagons
    path('wagons/types', WagonTypesView.as_view(), name='wagon_types'),
    path('wagons/<str:type>', WagonListView.as_view(), name='wagon_list'),
    path('wagons/<str:type>/create/', WagonCreateView.as_view(), name='wagon_create'),
    path('wagons/<str:type>/<int:pk>/', WagonDetailView.as_view(), name='wagon_detail'),
    path('wagons/<str:type>/<int:pk>/update/', WagonUpdateView.as_view(), name='wagon_update'),
    path('wagons/<str:type>/<int:pk>/delete/', WagonDeleteView.as_view(), name='wagon_delete'),

]