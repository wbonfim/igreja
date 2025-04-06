from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser deve ter is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractUser):
    username = None  # Remove o campo username
    email = models.EmailField('E-mail', unique=True)
    nome = models.CharField('Nome', max_length=150)
    cpf = models.CharField('CPF', max_length=11, unique=True)
    data_nascimento = models.DateField('Data de Nascimento', null=True, blank=True)
    telefone = models.CharField('Telefone', max_length=20, null=True, blank=True)
    endereco = models.CharField('Endereço', max_length=200, null=True, blank=True)
    cidade = models.CharField('Cidade', max_length=100, null=True, blank=True)
    estado = models.CharField('Estado', max_length=2, null=True, blank=True)
    cep = models.CharField('CEP', max_length=8, null=True, blank=True)
    data_criacao = models.DateTimeField('Data de Criação', auto_now_add=True)
    ultima_atualizacao = models.DateTimeField('Última Atualização', auto_now=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'cpf']

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.email
