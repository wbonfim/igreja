from django.db import models
from apps.autenticacao.models import Usuario
from apps.igrejas.models import Igreja

class EstadoCivil(models.TextChoices):
    SOLTEIRO = 'SO', 'Solteiro(a)'
    CASADO = 'CA', 'Casado(a)'
    DIVORCIADO = 'DI', 'Divorciado(a)'
    VIUVO = 'VI', 'Viúvo(a)'
    OUTROS = 'OU', 'Outros'

class Membro(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='perfil_membro'
    )
    igreja = models.ForeignKey(
        Igreja,
        on_delete=models.CASCADE,
        related_name='membros'
    )
    # Informações Pessoais
    nome_completo = models.CharField(max_length=200)
    data_nascimento = models.DateField(null=True, blank=True)
    rg = models.CharField(max_length=20, null=True, blank=True)
    cpf = models.CharField(max_length=11, unique=True, null=True, blank=True)
    estado_civil = models.CharField(
        max_length=2,
        choices=EstadoCivil.choices,
        default=EstadoCivil.SOLTEIRO
    )
    profissao = models.CharField(max_length=100, null=True, blank=True)

    # Contato
    telefone = models.CharField(max_length=20, null=True, blank=True)
    telefone_alternativo = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    # Endereço
    cep = models.CharField(max_length=8, null=True, blank=True)
    endereco = models.CharField(max_length=255, null=True, blank=True)
    numero = models.CharField(max_length=10, null=True, blank=True)
    complemento = models.CharField(max_length=100, null=True, blank=True)
    bairro = models.CharField(max_length=100, null=True, blank=True)
    cidade = models.CharField(max_length=100, null=True, blank=True)
    estado = models.CharField(max_length=2, null=True, blank=True)

    # Informações Eclesiásticas
    data_batismo = models.DateField(null=True, blank=True)
    data_membro = models.DateField(null=True, blank=True)
    cargo_ministerial = models.CharField(max_length=100, null=True, blank=True)

    # Informações Familiares
    nome_pai = models.CharField(max_length=200, null=True, blank=True)
    nome_mae = models.CharField(max_length=200, null=True, blank=True)
    nome_conjugue = models.CharField(max_length=200, null=True, blank=True)
    data_casamento = models.DateField(null=True, blank=True)

    # Observações e Histórico
    observacoes = models.TextField(null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Membro'
        verbose_name_plural = 'Membros'
        ordering = ['nome_completo']

    def __str__(self):
        return self.nome_completo

class HistoricoVisita(models.Model):
    membro = models.ForeignKey(
        Membro,
        on_delete=models.CASCADE,
        related_name='historico_visitas'
    )
    igreja_visitada = models.ForeignKey(
        Igreja,
        on_delete=models.CASCADE,
        related_name='visitas_recebidas'
    )
    data_visita = models.DateField()
    observacoes = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Histórico de Visita'
        verbose_name_plural = 'Histórico de Visitas'
        ordering = ['-data_visita']

    def __str__(self):
        return f"{self.membro.nome_completo} - {self.igreja_visitada.nome} - {self.data_visita}"

class Ministerio(models.Model):
    nome = models.CharField(max_length=100)
    igreja = models.ForeignKey(
        Igreja,
        on_delete=models.CASCADE,
        related_name='ministerios'
    )
    descricao = models.TextField()
    lider = models.ForeignKey(
        Membro,
        on_delete=models.SET_NULL,
        null=True,
        related_name='ministerios_liderados'
    )
    membros = models.ManyToManyField(
        Membro,
        related_name='ministerios_participantes'
    )
    data_criacao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Ministério'
        verbose_name_plural = 'Ministérios'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.igreja.nome}"
