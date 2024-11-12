from django.core.exceptions import ValidationError


class RouteStationValidator:
    def __init__(self, route_station):
        self.route_station = route_station
        self.route = route_station.route
        self.errors = []

    def validate(self):
        self.validate_unique_station_per_route()
        self.validate_unique_order_per_route()
        self.validate_arrival_before_departure()
        self.validate_previous_station()
        self.validate_next_station()

        if self.errors:
            raise ValidationError(self.errors)

    def validate_unique_station_per_route(self):
        if self.route_station.__class__.objects.filter(
            route=self.route,
            station=self.route_station.station
        ).exclude(pk=self.route_station.pk).exists():
            raise ValidationError({
                'station': 'Station must be unique per route.'
            })

    def validate_unique_order_per_route(self):
        if self.route_station.__class__.objects.filter(
            route=self.route,
            order=self.route_station.order
        ).exclude(pk=self.route_station.pk).exists():
            raise ValidationError({
                'order': 'Order must be unique per route.'
            })

    def validate_arrival_before_departure(self):
        if self.route_station.arrival_time >= self.route_station.departure_time:
            raise ValidationError({
                'arrival_time': 'Arrival time must be before departure time.'
            })

    def validate_previous_station(self):
        previous_station = self._get_previous_station()

        if (previous_station and
                self.route_station.arrival_time <= previous_station.departure_time):
            raise ValidationError({
                'arrival_time': f"Arrival time ({self.route_station.arrival_time}) "
                                f"must be after the departure time of the previous station "
                                f"{previous_station.station.name} ({previous_station.departure_time})."
            })

    def validate_next_station(self):
        next_station = self._get_next_station()

        if (next_station and
                self.route_station.departure_time >= next_station.arrival_time):
            raise ValidationError({
                'departure_time': f"Departure time ({self.route_station.departure_time}"
                                f"must be before the arrival time of the next station "
                                f" {next_station.station.name} ({next_station.arrival_time})."
            })

    def _get_previous_station(self):
        return self.route_station.__class__.objects.filter(
            route=self.route,
            order__lt=self.route_station.order
        ).order_by('-order').first()

    def _get_next_station(self):
        return self.route_station.__class__.objects.filter(
            route=self.route,
            order__gt=self.route_station.order
        ).order_by('order').first()