from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class Command(BaseCommand):
    help = 'Cria um usuário administrador padrão'

    def handle(self, *args, **kwargs):
        if not Usuario.objects.filter(email='admin@igreja.com').exists():
            Usuario.objects.create_superuser(
                email='admin@igreja.com',
                password='admin123',
                nome='Administrador',
                cpf='00000000000',
                is_staff=True,
                is_superuser=True,
                is_active=True
            )
            self.stdout.write(
                self.style.SUCCESS('Usuário administrador criado com sucesso!')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Usuário administrador já existe.')
            )
