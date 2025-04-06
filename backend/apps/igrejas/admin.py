from django.contrib import admin
from .models import Igreja, TemplateIgreja

@admin.register(TemplateIgreja)
class TemplateIgrejaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Igreja)
class IgrejaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cidade', 'estado', 'telefone')
    search_fields = ('nome', 'cidade', 'bairro')
    list_filter = ('estado',)

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'template')
        }),
        ('Mídia', {
            'fields': ('logo', 'imagem_fundo', 'video_fundo'),
            'description': 'Upload de imagens e vídeos para personalização do site'
        }),
        ('Localização', {
            'fields': ('endereco', 'bairro', 'cidade', 'estado', 'cep')
        }),
        ('Contato', {
            'fields': ('telefone', 'email')
        }),
        ('Redes Sociais', {
            'fields': ('facebook', 'instagram', 'youtube'),
            'classes': ('collapse',)
        }),
        ('Horários', {
            'fields': ('horario_cultos',),
            'description': 'Informe os horários dos cultos, um por linha'
        }),
        ('Financeiro', {
            'fields': ('saldo',),
            'classes': ('collapse',)
        }),
    )
