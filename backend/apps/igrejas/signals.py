from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Igreja, ConfiguracaoIgreja

@receiver(post_save, sender=Igreja)
def criar_configuracao_igreja(sender, instance, created, **kwargs):
    """
    Cria uma configuração padrão quando uma nova igreja é criada
    """
    if created:
        ConfiguracaoIgreja.objects.create(
            igreja=instance,
            horarios_culto=[],
            redes_sociais={},
            configuracoes_personalizadas={}
        )
