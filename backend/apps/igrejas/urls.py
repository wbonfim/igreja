from django.urls import path
from . import views

app_name = 'igrejas'

urlpatterns = [
    path('', views.index, name='index'),
    path('igreja/site/<int:igreja_id>/', views.igreja_site, name='igreja_site'),
]
