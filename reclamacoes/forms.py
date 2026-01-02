from django import forms
from .models import Empresa, Reclamacao, Denuncia

class EmpresaForm(forms.ModelForm):
    class Meta():
        model = Empresa
        fields = ['nome', 'cnpj']  

class ReclamacaoForm(forms.ModelForm):
    class Meta():
        model = Reclamacao
        fields = ['titulo','descricao',]