from django.db import models
from apps.igrejas.models import Igreja
from apps.membros.models import Membro

class Categoria(models.Model):
    TIPO_CHOICES = (
        ('E', 'Entrada'),
        ('S', 'Saída'),
    )

    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

class Entrada(models.Model):
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"

    class Meta:
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'

class Saida(models.Model):
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"

    class Meta:
        verbose_name = 'Saída'
        verbose_name_plural = 'Saídas'

class Dizimo(models.Model):
    membro = models.ForeignKey(Membro, on_delete=models.PROTECT)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Dízimo de {self.membro.nome_completo} - R$ {self.valor}"

    class Meta:
        verbose_name = 'Dízimo'
        verbose_name_plural = 'Dízimos'

class Oferta(models.Model):
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Oferta: {self.descricao} - R$ {self.valor}"

    class Meta:
        verbose_name = 'Oferta'
        verbose_name_plural = 'Ofertas'
