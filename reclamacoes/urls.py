from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('cadastrarempresa/',views.cadastrar_empresa,name='cadastrar_empresa'),
    path('reclame/<int:empresa_id>/', views.criar_reclamacao, name='criar_reclamacao'),
    path('vermais/<int:empresa_id>/', views.ver_mais_empresa, name='ver_mais_empresa'),
    
]