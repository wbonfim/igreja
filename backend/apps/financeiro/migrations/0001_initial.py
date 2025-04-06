from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('igrejas', '0001_initial'),
        ('membros', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('tipo', models.CharField(choices=[('R', 'Receita'), ('D', 'Despesa')], max_length=1)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('ultima_atualizacao', models.DateTimeField(auto_now=True)),
                ('ativo', models.BooleanField(default=True)),
                ('igreja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categorias', to='igrejas.igreja')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Transacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('R', 'Receita'), ('D', 'Despesa')], max_length=1)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data', models.DateField()),
                ('descricao', models.TextField(blank=True, null=True)),
                ('comprovante', models.FileField(blank=True, null=True, upload_to='comprovantes/')),
                ('forma_pagamento', models.CharField(choices=[('DI', 'Dinheiro'), ('PI', 'Pix'), ('CC', 'Cartão de Crédito'), ('CD', 'Cartão de Débito'), ('BO', 'Boleto'), ('TR', 'Transferência')], max_length=2)),
                ('status', models.CharField(choices=[('PE', 'Pendente'), ('EF', 'Efetivado'), ('CA', 'Cancelado')], default='PE', max_length=2)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('ultima_atualizacao', models.DateTimeField(auto_now=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transacoes', to='financeiro.categoria')),
                ('igreja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transacoes', to='igrejas.igreja')),
                ('membro', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transacoes', to='membros.membro')),
            ],
            options={
                'verbose_name': 'Transação',
                'verbose_name_plural': 'Transações',
                'ordering': ['-data', '-data_criacao'],
            },
        ),
    ]
