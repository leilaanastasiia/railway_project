from django.contrib import admin

from railway.models import RailwayStation, Train, Route

admin.site.register(RailwayStation)
admin.site.register(Train)
admin.site.register(Route)
