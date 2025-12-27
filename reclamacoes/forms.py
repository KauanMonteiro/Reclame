from django import forms
from .models import Empresa, Reclamacao, Denuncia

class EmpresaForm(forms.ModelForm):
    class Meta():
        model = Empresa
        fields = ['nome', 'cnpj']  