from django.urls import path
from . import views
app_name = 'usuarios'  

urlpatterns = [
    path('registro/', views.cadastro_view, name='registro'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout, name='logout'),
]