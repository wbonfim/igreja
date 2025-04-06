from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

app_name = 'autenticacao'

urlpatterns = [
    # Autenticação JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Registro e gerenciamento de usuários
    path('registro/', views.RegistroUsuarioView.as_view(), name='registro'),
    path('perfil/', views.PerfilUsuarioView.as_view(), name='perfil'),
    path('alterar-senha/', views.AlterarSenhaView.as_view(), name='alterar_senha'),
    path('usuarios/', views.ListaUsuariosView.as_view(), name='lista_usuarios'),
    path('usuarios/<int:pk>/', views.DetalheUsuarioView.as_view(), name='detalhe_usuario'),
    
    # Níveis de acesso
    path('niveis-acesso/', views.NiveisAcessoView.as_view(), name='niveis_acesso'),
    path('verificar-permissao/<str:nivel>/', views.VerificarPermissaoView.as_view(), name='verificar_permissao'),
    
    # Recuperação de senha
    path('recuperar-senha/', views.RecuperarSenhaView.as_view(), name='recuperar_senha'),
    path('redefinir-senha/<str:token>/', views.RedefinirSenhaView.as_view(), name='redefinir_senha'),
]
