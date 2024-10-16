from django.urls import path

from railway.views import RouteListView, RouteDetailView, RouteCreateView, RouteUpdateView, RouteDeleteView, \
    StationListView, StationDetailView, StationCreateView, StationUpdateView, StationDeleteView, TrainListView, \
    TrainDetailView, TrainCreateView, TrainUpdateView, TrainDeleteView

app_name = 'railway'

urlpatterns = [
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
    path('trains/<int:pk>/delete/', TrainDeleteView.as_view(), name='train_delete'),
]