from django.db import models
from django.conf import settings

class Igreja(models.Model):
    nome = models.CharField(max_length=200)
    endereco = models.CharField(max_length=500)
    bairro = models.CharField(max_length=200, blank=True, null=True)
    cidade = models.CharField(max_length=200)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=9)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    cnpj = models.CharField(max_length=18, blank=True, null=True)
    data_fundacao = models.DateField(blank=True, null=True)
    pastor_responsavel = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='igrejas_como_pastor'
    )
    saldo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # Campos de mídia
    logo = models.ImageField(
        upload_to='igrejas/logos/',
        blank=True,
        null=True
    )
    imagem_fundo = models.ImageField(
        upload_to='igrejas/backgrounds/',
        blank=True,
        null=True
    )
    video_fundo = models.FileField(
        upload_to='igrejas/videos/',
        blank=True,
        null=True
    )

    # Campos de template
    template = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    cor_primaria = models.CharField(
        max_length=7,
        default='#007bff'
    )
    cor_secundaria = models.CharField(
        max_length=7,
        default='#6c757d'
    )

    class Meta:
        verbose_name = 'Igreja'
        verbose_name_plural = 'Igrejas'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        # Criar diretório para mídia se não existir
        import os
        from django.conf import settings

        media_dirs = [
            os.path.join(settings.MEDIA_ROOT, 'igrejas/logos'),
            os.path.join(settings.MEDIA_ROOT, 'igrejas/backgrounds'),
            os.path.join(settings.MEDIA_ROOT, 'igrejas/videos')
        ]

        for directory in media_dirs:
            if not os.path.exists(directory):
                os.makedirs(directory)

        super().save(*args, **kwargs)
