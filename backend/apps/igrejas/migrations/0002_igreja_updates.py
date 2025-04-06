from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('igrejas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='igreja',
            name='saldo',
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=12,
                verbose_name='Saldo'
            ),
        ),
        migrations.AddField(
            model_name='igreja',
            name='bairro',
            field=models.CharField(
                max_length=100,
                default='Centro'
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='templateigreja',
            name='tipo',
            field=models.CharField(
                choices=[
                    ('moderno', 'Moderno'),
                    ('tradicional', 'Tradicional'),
                    ('minimalista', 'Minimalista'),
                    ('contemporaneo', 'Contemporâneo')
                ],
                default='moderno',
                max_length=20
            ),
        ),
        migrations.AddField(
            model_name='templateigreja',
            name='html_padrao',
            field=models.TextField(
                default='',
                help_text='HTML base do template'
            ),
        ),
        migrations.AddField(
            model_name='templateigreja',
            name='css_padrao',
            field=models.TextField(
                default='',
                help_text='CSS base do template'
            ),
        ),
        migrations.AddField(
            model_name='templateigreja',
            name='js_padrao',
            field=models.TextField(
                default='',
                help_text='JavaScript base do template'
            ),
        ),
        migrations.AlterField(
            model_name='templateigreja',
            name='configuracao',
            field=models.JSONField(
                default=dict,
                help_text='Configurações do template em formato JSON'
            ),
        ),
    ]
