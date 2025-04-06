from django.apps import AppConfig

class IgrejasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.igrejas'
    verbose_name = 'Igrejas'

    def ready(self):
        import apps.igrejas.signals  # noqa
