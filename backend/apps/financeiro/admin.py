from django.contrib import admin
from .models import Entrada, Saida, Categoria, Dizimo, Oferta

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'igreja')
    list_filter = ('tipo', 'igreja')
    search_fields = ('nome',)

@admin.register(Entrada)
class EntradaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'data', 'categoria', 'igreja')
    list_filter = ('data', 'categoria', 'igreja')
    search_fields = ('descricao',)
    date_hierarchy = 'data'

@admin.register(Saida)
class SaidaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'data', 'categoria', 'igreja')
    list_filter = ('data', 'categoria', 'igreja')
    search_fields = ('descricao',)
    date_hierarchy = 'data'

@admin.register(Dizimo)
class DizimoAdmin(admin.ModelAdmin):
    list_display = ('membro', 'valor', 'data', 'igreja')
    list_filter = ('data', 'igreja', 'membro')
    search_fields = ('membro__nome_completo',)
    date_hierarchy = 'data'

@admin.register(Oferta)
class OfertaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'data', 'igreja')
    list_filter = ('data', 'igreja')
    search_fields = ('descricao',)
    date_hierarchy = 'data'
