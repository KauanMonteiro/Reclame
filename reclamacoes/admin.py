from kivy.uix.behaviors.cover import Decimal
from django.contrib import admin
from .models import Empresa,Reclamacao,Denuncia


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    pass


@admin.register(Reclamacao)
class ReclamacaoAdmin(admin.ModelAdmin):
    pass

@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    pass