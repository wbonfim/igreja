from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.conf import settings

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """
    View para a raiz da API que lista todos os endpoints disponíveis
    """
    return Response({
        'status': 'online',
        'version': settings.VERSION if hasattr(settings, 'VERSION') else '1.0.0',
        'environment': 'Development' if settings.DEBUG else 'Production',
        'endpoints': {
            'auth': {
                'description': 'Endpoints de autenticação e gerenciamento de usuários',
                'endpoints': {
                    'login': request.build_absolute_uri('/api/auth/token/'),
                    'refresh': request.build_absolute_uri('/api/auth/token/refresh/'),
                    'registro': request.build_absolute_uri('/api/auth/registro/'),
                    'perfil': request.build_absolute_uri('/api/auth/perfil/'),
                }
            },
            'igrejas': {
                'description': 'Gerenciamento de igrejas e congregações',
                'url': request.build_absolute_uri('/api/igrejas/'),
            },
            'membros': {
                'description': 'Gerenciamento de membros e visitantes',
                'url': request.build_absolute_uri('/api/membros/'),
            },
            'financeiro': {
                'description': 'Gestão financeira, incluindo receitas, despesas e relatórios',
                'url': request.build_absolute_uri('/api/financeiro/'),
            },
            'admin': {
                'description': 'Interface administrativa do Django',
                'url': request.build_absolute_uri('/admin/'),
            },
            'docs': {
                'description': 'Documentação da API',
                'url': request.build_absolute_uri('/docs/'),
            }
        }
    })
