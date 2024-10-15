from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from railway.models import RailwayStation, Route, Train, CustomUser, Ticket


class RailwayStationAdmin(admin.ModelAdmin):
    list_display = ('name', )


class RouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    filter_horizontal = ('stations',)


class TrainAdmin(admin.ModelAdmin):
    list_display = ('number', 'type', 'route', 'station')
    list_filter = ('type', 'route', 'station')


class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'train', 'start_station', 'end_station', 'user')
    list_filter = ('train', 'start_station', 'end_station')


admin.site.register(RailwayStation, RailwayStationAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Train, TrainAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(CustomUser)
