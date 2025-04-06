from django.urls import path
from . import views

app_name = 'membros'

urlpatterns = [
    # Gerenciamento de membros
    path('', views.ListaMembrosView.as_view(), name='lista_membros'),
    path('<int:pk>/', views.DetalheMembrosView.as_view(), name='detalhe_membro'),
    path('criar/', views.CriarMembroView.as_view(), name='criar_membro'),
    path('<int:pk>/atualizar/', views.AtualizarMembroView.as_view(), name='atualizar_membro'),
    path('<int:pk>/excluir/', views.ExcluirMembroView.as_view(), name='excluir_membro'),
    
    # Listagens específicas
    path('ativos/', views.MembrosAtivosView.as_view(), name='membros_ativos'),
    path('inativos/', views.MembrosInativosView.as_view(), name='membros_inativos'),
    path('aniversariantes/', views.AniversariantesView.as_view(), name='aniversariantes'),
    
    # Ministérios
    path('ministerios/', views.ListaMinisteriosView.as_view(), name='lista_ministerios'),
    path('ministerios/<int:pk>/', views.DetalheMinisterioView.as_view(), name='detalhe_ministerio'),
    path('ministerios/criar/', views.CriarMinisterioView.as_view(), name='criar_ministerio'),
    path('ministerios/<int:pk>/membros/', views.MembrosMinisterioView.as_view(), name='membros_ministerio'),
    
    # Histórico de visitas
    path('visitas/', views.ListaVisitasView.as_view(), name='lista_visitas'),
    path('visitas/criar/', views.RegistrarVisitaView.as_view(), name='registrar_visita'),
    path('visitas/<int:pk>/', views.DetalheVisitaView.as_view(), name='detalhe_visita'),
    
    # Relatórios
    path('relatorios/geral/', views.RelatorioGeralView.as_view(), name='relatorio_geral'),
    path('relatorios/ministerios/', views.RelatorioMinisteriosView.as_view(), name='relatorio_ministerios'),
    path('relatorios/visitas/', views.RelatorioVisitasView.as_view(), name='relatorio_visitas'),
    
    # Exportação
    path('exportar/csv/', views.ExportarCSVView.as_view(), name='exportar_csv'),
    path('exportar/pdf/', views.ExportarPDFView.as_view(), name='exportar_pdf'),
    
    # Busca e filtros
    path('buscar/', views.BuscarMembrosView.as_view(), name='buscar_membros'),
    path('filtrar/', views.FiltrarMembrosView.as_view(), name='filtrar_membros'),
    
    # Carteirinha de membro
    path('<int:pk>/carteirinha/', views.CarteirinhaMembrosView.as_view(), name='carteirinha_membro'),
    path('carteirinhas/lote/', views.GerarCarteirinhasLoteView.as_view(), name='carteirinhas_lote')
]
