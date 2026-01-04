from django import forms
from .models import Empresa, Reclamacao, Denuncia

class EmpresaForm(forms.ModelForm):
    class Meta():
        model = Empresa
        fields = ['nome', 'cnpj']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-input', 'inputmode': 'numeric','maxlength': '14','placeholder': 'Digite apenas números'}),
        }

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        if not cnpj.isdigit():
            raise forms.ValidationError("O CNPJ deve conter apenas números.")
        if len(cnpj) != 14:
            raise forms.ValidationError("O CNPJ deve conter exatamente 14 números.")
        return cnpj
    
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