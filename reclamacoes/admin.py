from django.contrib import admin
from .models import Empresa,Reclamacao


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    pass


@admin.register(Reclamacao)
class ReclamacaoAdmin(admin.ModelAdmin):
    pass