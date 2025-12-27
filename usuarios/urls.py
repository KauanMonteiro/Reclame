from django.urls import path
from . import views
app_name = 'usuarios'

urlpatterns = [
    path('registro/', views.cadastro_view, name='registro'),
    path('concluir_cadastro/', views.concluir_cadastro, name='concluir_cadastro'),
]