from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Membro

@receiver(post_save, sender=Membro)
def configurar_membro(sender, instance, created, **kwargs):
    """
    Configura um membro após sua criação
    """
    if created:
        # Implementar a lógica de configuração inicial do membro aqui
        pass
