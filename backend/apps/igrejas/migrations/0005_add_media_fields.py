from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('igrejas', '0004_template_igreja_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='igreja',
            name='logo',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='igrejas/logos/',
                verbose_name='Logo'
            ),
        ),
        migrations.AddField(
            model_name='igreja',
            name='imagem_fundo',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='igrejas/backgrounds/',
                verbose_name='Imagem de Fundo'
            ),
        ),
        migrations.AddField(
            model_name='igreja',
            name='video_fundo',
            field=models.FileField(
                blank=True,
                null=True,
                upload_to='igrejas/videos/',
                verbose_name='Vídeo de Fundo',
                help_text='Formatos suportados: MP4, WebM'
            ),
        ),
        migrations.AddField(
            model_name='igreja',
            name='facebook',
            field=models.URLField(
                blank=True,
                verbose_name='Facebook'
            ),
        ),
        migrations.AddField(
            model_name='igreja',
            name='instagram',
            field=models.URLField(
                blank=True,
                verbose_name='Instagram'
            ),
        ),
        migrations.AddField(
            model_name='igreja',
            name='youtube',
            field=models.URLField(
                blank=True,
                verbose_name='YouTube'
            ),
        ),
        migrations.AddField(
            model_name='igreja',
            name='horario_cultos',
            field=models.TextField(
                blank=True,
                verbose_name='Horários dos Cultos',
                help_text='Ex: Domingo - 18h00\nQuarta - 19h30'
            ),
        ),
    ]
