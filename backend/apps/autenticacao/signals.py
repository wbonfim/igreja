from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Usuario
from apps.membros.models import Membro
from apps.igrejas.models import Igreja

@receiver(post_save, sender=Usuario)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    """
    Cria um perfil de membro automaticamente quando um novo usuário é criado
    """
    if created and not hasattr(instance, 'perfil_membro'):
        # Busca a igreja padrão
        igreja = Igreja.objects.filter(nome='Igreja Principal').first()

        if igreja:
            # Cria o perfil do membro com a igreja padrão
            Membro.objects.create(
                usuario=instance,
                igreja=igreja,
                nome_completo=instance.get_full_name() or instance.username,
                email=instance.email,
                estado_civil='SO'  # Estado civil padrão: Solteiro
            )
