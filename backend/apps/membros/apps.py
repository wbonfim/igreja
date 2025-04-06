from django.apps import AppConfig

class MembrosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.membros'
    verbose_name = 'Membros'

    def ready(self):
        import apps.membros.signals  # noqa
