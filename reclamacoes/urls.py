from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('cadastrarempresa/',views.cadastrar_empresa,name='cadastrar_empresa'),
    path('reclame/<int:empresa_id>/', views.criar_reclamacao, name='criar_reclamacao'),
    path('vermais/<int:empresa_id>/', views.ver_mais_empresa, name='ver_mais_empresa'),
    path('vermais/reclamacao/<int:reclamacao_id>/',views.ver_mais_reclamacao,name='ver_mais_reclamacao'),
    path('area_admin/',views.area_admin,name='area_admin'),
    path('denunciar/<int:reclamacao_id>/',views.denunciar,name="denunciar"),
    path('bloquear/<int:reclamacao_id>/',views.bloquear,name='bloquear'),
    path('desbloquear/<int:reclamacao_id>/',views.desbloquear,name='desbloquear'),
    path('aprovar/<int:empresa_id>/', views.aprovar, name='aprovar'),
    path('rejeitar/<int:empresa_id>/', views.rejeitar, name='rejeitar'),
    path('registro/', views.cadastro_usuario, name='registro'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout, name='logout'),
]