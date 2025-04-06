from django.contrib import admin
from .models import Membro

@admin.register(Membro)
class MembroAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'igreja', 'email', 'telefone', 'ativo')
    list_filter = ('ativo', 'igreja', 'estado_civil')
    search_fields = ('nome_completo', 'email', 'cpf')
    readonly_fields = ('data_criacao', 'ultima_atualizacao')
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('usuario', 'igreja', 'nome_completo', 'data_nascimento', 'estado_civil')
        }),
        ('Contato', {
            'fields': ('email', 'telefone', 'telefone_alternativo')
        }),
        ('Documentos', {
            'fields': ('rg', 'cpf')
        }),
        ('Endereço', {
            'fields': ('cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado')
        }),
        ('Informações Eclesiásticas', {
            'fields': ('data_batismo', 'data_membro', 'cargo_ministerial')
        }),
        ('Família', {
            'fields': ('nome_pai', 'nome_mae', 'nome_conjugue', 'data_casamento')
        }),
        ('Observações', {
            'fields': ('observacoes',)
        }),
        ('Status', {
            'fields': ('ativo', 'data_criacao', 'ultima_atualizacao')
        }),
    )
