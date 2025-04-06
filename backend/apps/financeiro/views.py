from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Entrada, Saida, Categoria, Dizimo, Oferta
from .serializers import (
    EntradaSerializer,
    SaidaSerializer,
    CategoriaSerializer,
    DizimoSerializer,
    OfertaSerializer
)

class CategoriaViewSet(viewsets.ModelViewSet):
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Categoria.objects.filter(igreja=self.request.user.igreja)

    def perform_create(self, serializer):
        serializer.save(igreja=self.request.user.igreja)

class EntradaViewSet(viewsets.ModelViewSet):
    serializer_class = EntradaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Entrada.objects.filter(igreja=self.request.user.igreja)

    def perform_create(self, serializer):
        serializer.save(igreja=self.request.user.igreja)

class SaidaViewSet(viewsets.ModelViewSet):
    serializer_class = SaidaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Saida.objects.filter(igreja=self.request.user.igreja)

    def perform_create(self, serializer):
        serializer.save(igreja=self.request.user.igreja)

class DizimoViewSet(viewsets.ModelViewSet):
    serializer_class = DizimoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Dizimo.objects.filter(igreja=self.request.user.igreja)

    def perform_create(self, serializer):
        serializer.save(igreja=self.request.user.igreja)

class OfertaViewSet(viewsets.ModelViewSet):
    serializer_class = OfertaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Oferta.objects.filter(igreja=self.request.user.igreja)

    def perform_create(self, serializer):
        serializer.save(igreja=self.request.user.igreja)

    @action(detail=False, methods=['get'])
    def resumo_financeiro(self, request):
        igreja = request.user.igreja
        hoje = timezone.now().date()
        inicio_mes = hoje.replace(day=1)
        fim_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        # Totais do mês atual
        entradas_mes = Entrada.objects.filter(
            igreja=igreja,
            data__range=[inicio_mes, fim_mes]
        ).aggregate(total=Sum('valor'))['total'] or 0

        saidas_mes = Saida.objects.filter(
            igreja=igreja,
            data__range=[inicio_mes, fim_mes]
        ).aggregate(total=Sum('valor'))['total'] or 0

        dizimos_mes = Dizimo.objects.filter(
            igreja=igreja,
            data__range=[inicio_mes, fim_mes]
        ).aggregate(total=Sum('valor'))['total'] or 0

        ofertas_mes = Oferta.objects.filter(
            igreja=igreja,
            data__range=[inicio_mes, fim_mes]
        ).aggregate(total=Sum('valor'))['total'] or 0

        # Saldo atual
        saldo_atual = igreja.saldo

        return Response({
            'saldo_atual': saldo_atual,
            'mes_atual': {
                'entradas': entradas_mes,
                'saidas': saidas_mes,
                'dizimos': dizimos_mes,
                'ofertas': ofertas_mes,
                'saldo': entradas_mes + dizimos_mes + ofertas_mes - saidas_mes
            }
        })
