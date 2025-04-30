from django.contrib import admin
from django.urls import include, path
import reclamacoes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('reclamacoes.urls'))
]
