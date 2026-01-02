from django import forms
from .models import Empresa, Reclamacao, Denuncia

class EmpresaForm(forms.ModelForm):
    class Meta():
        model = Empresa
        fields = ['nome', 'cnpj']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-input'}),
        }

class ReclamacaoForm(forms.ModelForm):
    class Meta():
        model = Reclamacao
        fields = ['titulo','descricao',]
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-input'}),
            'descricao': forms.Textarea(attrs={'class': 'form-input'}),
        }

class DenunciaForm(forms.ModelForm):
    class Meta():
        model = Denuncia
        fields = ['motivo', 'comentario']
        widgets = {
            'motivo': forms.Select(attrs={'class': 'form-input'}),
            'comentario': forms.Textarea(attrs={'class': 'form-input'}),
        }