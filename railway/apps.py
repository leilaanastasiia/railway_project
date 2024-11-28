from django.apps import AppConfig


class RailwayConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'railway'

    def ready(self):
        from railway import signals