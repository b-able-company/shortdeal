from django.apps import AppConfig


class LoiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.loi'
    verbose_name = 'LOI 관리'

    def ready(self):
        import apps.loi.signals  # noqa
