from django.core.management.base import BaseCommand
from apps.igrejas.models import Igreja
from django.utils import timezone

class Command(BaseCommand):
    help = 'Cria uma igreja padrão para o sistema'

    def handle(self, *args, **kwargs):
        if not Igreja.objects.filter(nome='Igreja Principal').exists():
            igreja = Igreja.objects.create(
                nome='Igreja Principal',
                endereco='Endereço Padrão',
                cidade='Cidade',
                estado='SP',
                cep='00000000',
                telefone='0000000000',
                email='igreja@example.com',
                data_fundacao=timezone.now().date(),
                descricao='Igreja Principal do Sistema',
                ativa=True
            )
            self.stdout.write(self.style.SUCCESS(f'Igreja padrão criada com ID {igreja.id}'))
        else:
            self.stdout.write(self.style.SUCCESS('Igreja padrão já existe'))
