from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('autenticacao', '0001_initial'),
        ('igrejas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_completo', models.CharField(max_length=200)),
                ('data_nascimento', models.DateField(blank=True, null=True)),
                ('rg', models.CharField(blank=True, max_length=20, null=True)),
                ('cpf', models.CharField(blank=True, max_length=11, null=True, unique=True)),
                ('estado_civil', models.CharField(choices=[('SO', 'Solteiro(a)'), ('CA', 'Casado(a)'), ('DI', 'Divorciado(a)'), ('VI', 'Viúvo(a)'), ('OU', 'Outros')], default='SO', max_length=2)),
                ('profissao', models.CharField(blank=True, max_length=100, null=True)),
                ('telefone', models.CharField(blank=True, max_length=20, null=True)),
                ('telefone_alternativo', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('cep', models.CharField(blank=True, max_length=8, null=True)),
                ('endereco', models.CharField(blank=True, max_length=255, null=True)),
                ('numero', models.CharField(blank=True, max_length=10, null=True)),
                ('complemento', models.CharField(blank=True, max_length=100, null=True)),
                ('bairro', models.CharField(blank=True, max_length=100, null=True)),
                ('cidade', models.CharField(blank=True, max_length=100, null=True)),
                ('estado', models.CharField(blank=True, max_length=2, null=True)),
                ('data_batismo', models.DateField(blank=True, null=True)),
                ('data_membro', models.DateField(blank=True, null=True)),
                ('cargo_ministerial', models.CharField(blank=True, max_length=100, null=True)),
                ('nome_pai', models.CharField(blank=True, max_length=200, null=True)),
                ('nome_mae', models.CharField(blank=True, max_length=200, null=True)),
                ('nome_conjugue', models.CharField(blank=True, max_length=200, null=True)),
                ('data_casamento', models.DateField(blank=True, null=True)),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('ultima_atualizacao', models.DateTimeField(auto_now=True)),
                ('ativo', models.BooleanField(default=True)),
                ('igreja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='membros', to='igrejas.igreja')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil_membro', to='autenticacao.usuario')),
            ],
            options={
                'verbose_name': 'Membro',
                'verbose_name_plural': 'Membros',
                'ordering': ['nome_completo'],
            },
        ),
        migrations.CreateModel(
            name='Ministerio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField()),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('ativo', models.BooleanField(default=True)),
                ('igreja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ministerios', to='igrejas.igreja')),
                ('lider', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ministerios_liderados', to='membros.membro')),
                ('membros', models.ManyToManyField(related_name='ministerios_participantes', to='membros.membro')),
            ],
            options={
                'verbose_name': 'Ministério',
                'verbose_name_plural': 'Ministérios',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='HistoricoVisita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_visita', models.DateField()),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('igreja_visitada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visitas_recebidas', to='igrejas.igreja')),
                ('membro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historico_visitas', to='membros.membro')),
            ],
            options={
                'verbose_name': 'Histórico de Visita',
                'verbose_name_plural': 'Histórico de Visitas',
                'ordering': ['-data_visita'],
            },
        ),
    ]
