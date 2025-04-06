from rest_framework import serializers
from .models import Entrada, Saida, Categoria, Dizimo, Oferta

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'tipo']
        read_only_fields = ['igreja']

class EntradaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrada
        fields = ['id', 'descricao', 'valor', 'data', 'categoria', 'observacoes']
        read_only_fields = ['igreja']

class SaidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saida
        fields = ['id', 'descricao', 'valor', 'data', 'categoria', 'observacoes']
        read_only_fields = ['igreja']

class DizimoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dizimo
        fields = ['id', 'membro', 'valor', 'data', 'observacoes']
        read_only_fields = ['igreja']

class OfertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oferta
        fields = ['id', 'descricao', 'valor', 'data', 'observacoes']
        read_only_fields = ['igreja']
