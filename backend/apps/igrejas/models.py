from django.db import models
from django.urls import reverse

class TemplateIgreja(models.Model):
    nome = models.CharField('Nome', max_length=100)
    html = models.TextField('HTML')
    css = models.TextField('CSS')
    js = models.TextField('JavaScript', blank=True)

    class Meta:
        verbose_name = 'Template'
        verbose_name_plural = 'Templates'

    def __str__(self):
        return self.nome

class Igreja(models.Model):
    nome = models.CharField('Nome', max_length=200)
    descricao = models.TextField('Descrição', blank=True)
    endereco = models.CharField('Endereço', max_length=200)
    bairro = models.CharField('Bairro', max_length=100)
    cidade = models.CharField('Cidade', max_length=100)
    estado = models.CharField('Estado', max_length=2)
    cep = models.CharField('CEP', max_length=8)
    telefone = models.CharField('Telefone', max_length=20)
    email = models.EmailField('E-mail')
    saldo = models.DecimalField('Saldo', max_digits=10, decimal_places=2, default=0)

    # Campos de mídia
    logo = models.ImageField('Logo', upload_to='igrejas/logos/', blank=True, null=True)
    imagem_fundo = models.ImageField('Imagem de Fundo', upload_to='igrejas/backgrounds/', blank=True, null=True)
    video_fundo = models.FileField('Vídeo de Fundo', upload_to='igrejas/videos/', blank=True, null=True, help_text='Formatos suportados: MP4, WebM')

    # Redes sociais
    facebook = models.URLField('Facebook', blank=True)
    instagram = models.URLField('Instagram', blank=True)
    youtube = models.URLField('YouTube', blank=True)

    # Horários
    horario_cultos = models.TextField('Horários dos Cultos', blank=True, help_text='Ex: Domingo - 18h00\nQuarta - 19h30')

    template = models.ForeignKey(TemplateIgreja, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Igreja'
        verbose_name_plural = 'Igrejas'

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('igreja_site', args=[str(self.id)])
