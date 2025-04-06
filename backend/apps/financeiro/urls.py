from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categorias', views.CategoriaViewSet, basename='categoria')
router.register(r'entradas', views.EntradaViewSet, basename='entrada')
router.register(r'saidas', views.SaidaViewSet, basename='saida')
router.register(r'dizimos', views.DizimoViewSet, basename='dizimo')
router.register(r'ofertas', views.OfertaViewSet, basename='oferta')

urlpatterns = [
    path('', include(router.urls)),
]
