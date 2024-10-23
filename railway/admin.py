from django.contrib import admin

from railway.models import RailwayStation, Route, Train, CustomUser, Ticket, SVWagon, CoupeWagon, PlatzWagon, \
    SittingWagon, TankWagon


@admin.register(RailwayStation)
class RailwayStationAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    filter_horizontal = ('stations',)


@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ('number', 'type', 'route', 'station')
    list_filter = ('type', 'route', 'station')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'train', 'start_station', 'end_station', 'user')
    list_filter = ('train', 'start_station', 'end_station')


@admin.register(SittingWagon)
@admin.register(PlatzWagon)
@admin.register(SVWagon)
@admin.register(CoupeWagon)
class PassWagonAdmin(admin.ModelAdmin):
    list_display = ('number', 'train', 'capacity')
    list_filter = ('train',)


@admin.register(TankWagon)
class CargoWagonAdmin(admin.ModelAdmin):
    list_display = ('number', 'train', 'max_liters')
    list_filter = ('train',)

admin.site.register(CustomUser)
