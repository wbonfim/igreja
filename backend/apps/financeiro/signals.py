from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Entrada, Saida, Dizimo, Oferta

@receiver([post_save, post_delete], sender=Entrada)
@receiver([post_save, post_delete], sender=Saida)
@receiver([post_save, post_delete], sender=Dizimo)
@receiver([post_save, post_delete], sender=Oferta)
def atualizar_saldo(sender, instance, **kwargs):
    """
    Atualiza o saldo da igreja quando houver movimentação financeira.
    """
    igreja = instance.igreja

    # Calcula total de entradas
    entradas = sum(
        entrada.valor
        for entrada in Entrada.objects.filter(igreja=igreja)
    )

    # Adiciona dízimos
    entradas += sum(
        dizimo.valor
        for dizimo in Dizimo.objects.filter(igreja=igreja)
    )

    # Adiciona ofertas
    entradas += sum(
        oferta.valor
        for oferta in Oferta.objects.filter(igreja=igreja)
    )

    # Calcula total de saídas
    saidas = sum(
        saida.valor
        for saida in Saida.objects.filter(igreja=igreja)
    )

    # Atualiza o saldo da igreja
    igreja.saldo = entradas - saidas
    igreja.save()
