from django.apps import AppConfig


class BoothsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.booths'

    def ready(self):
        """Import signals when app is ready"""
        import apps.booths.signals  # noqa
