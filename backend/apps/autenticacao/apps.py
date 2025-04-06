from django.apps import AppConfig

class AutenticacaoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.autenticacao'
    verbose_name = 'Autenticação'

    def ready(self):
        import apps.autenticacao.signals  # noqa
