from django.contrib import admin
from django.urls import include, path
import reclamacoes
import usuarios
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('reclamacoes.urls')),
    path('usuarios/',include('usuarios.urls'))
]
