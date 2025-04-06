from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='TemplateIgreja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField()),
                ('thumbnail', models.ImageField(upload_to='templates_thumbnails/')),
                ('configuracao', models.JSONField(help_text='Configurações do template em formato JSON')),
                ('ativo', models.BooleanField(default=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Template',
                'verbose_name_plural': 'Templates',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Igreja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=250, unique=True)),
                ('cnpj', models.CharField(blank=True, max_length=14, null=True, unique=True)),
                ('endereco', models.CharField(max_length=255)),
                ('cidade', models.CharField(max_length=100)),
                ('estado', models.CharField(max_length=2)),
                ('cep', models.CharField(max_length=8)),
                ('telefone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('site', models.URLField(blank=True, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logos_igrejas/')),
                ('data_fundacao', models.DateField(blank=True, null=True)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('ultima_atualizacao', models.DateTimeField(auto_now=True)),
                ('ativa', models.BooleanField(default=True)),
                ('igreja_sede', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='filiais', to='igrejas.igreja')),
                ('template_ativo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='igrejas', to='igrejas.templateigreja')),
            ],
            options={
                'verbose_name': 'Igreja',
                'verbose_name_plural': 'Igrejas',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='ConfiguracaoIgreja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horarios_culto', models.JSONField(default=list, help_text='Lista de horários dos cultos')),
                ('redes_sociais', models.JSONField(default=dict, help_text='Links das redes sociais')),
                ('configuracoes_personalizadas', models.JSONField(default=dict, help_text='Configurações personalizadas da igreja')),
                ('ultima_atualizacao', models.DateTimeField(auto_now=True)),
                ('igreja', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='configuracao', to='igrejas.igreja')),
            ],
            options={
                'verbose_name': 'Configuração da Igreja',
                'verbose_name_plural': 'Configurações das Igrejas',
            },
        ),
    ]
