from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Igreja
from django.conf import settings
import os

@receiver(pre_save, sender=Igreja)
def limpar_arquivos_antigos(sender, instance, **kwargs):
    """Remove arquivos antigos quando novos são enviados"""
    if instance.pk:  # Se é uma atualização
        try:
            old_instance = Igreja.objects.get(pk=instance.pk)

            # Verificar e remover logo antigo
            if old_instance.logo and old_instance.logo != instance.logo:
                if os.path.isfile(old_instance.logo.path):
                    os.remove(old_instance.logo.path)

            # Verificar e remover imagem de fundo antiga
            if old_instance.imagem_fundo and old_instance.imagem_fundo != instance.imagem_fundo:
                if os.path.isfile(old_instance.imagem_fundo.path):
                    os.remove(old_instance.imagem_fundo.path)

            # Verificar e remover vídeo de fundo antigo
            if old_instance.video_fundo and old_instance.video_fundo != instance.video_fundo:
                if os.path.isfile(old_instance.video_fundo.path):
                    os.remove(old_instance.video_fundo.path)

        except Igreja.DoesNotExist:
            pass

@receiver(post_save, sender=Igreja)
def criar_diretorios_midia(sender, instance, created, **kwargs):
    """Cria os diretórios necessários para armazenar os arquivos de mídia"""
    media_dirs = [
        os.path.join(settings.MEDIA_ROOT, 'igrejas/logos'),
        os.path.join(settings.MEDIA_ROOT, 'igrejas/backgrounds'),
        os.path.join(settings.MEDIA_ROOT, 'igrejas/videos')
    ]

    for directory in media_dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)
