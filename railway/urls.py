from django.urls import path

from railway.views import RouteListView, RouteDetailView, RouteCreateView, RouteUpdateView, RouteDeleteView

app_name = 'railway'

urlpatterns = [
    path('routes/', RouteListView.as_view(), name='routes'),
    path('routes/<int:pk>/', RouteDetailView.as_view(), name='route'),
    path('routes/add/', RouteCreateView.as_view(), name='route_create'),
    path('routes/<int:pk>/update/', RouteUpdateView.as_view(), name='route_update'),
    path('routes/<int:pk>/delete/', RouteDeleteView.as_view(), name='route_delete'),
]