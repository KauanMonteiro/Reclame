from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    if not regex.match(password):
        raise ValidationError(
            'A senha deve conter pelo menos uma letra maiúscula, '
            'uma letra minúscula, um número e ter no mínimo 8 caracteres.',
            code='invalid'
        )

class CadastroUsuarioForm(forms.ModelForm):
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
        validators=[strong_password]
    )    
    password2 = forms.CharField(
        label='confirme a sua senha',
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
        
    )

    class Meta:
        model = User
        fields = ['username','email','password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise ValidationError(
                {'password2':'As senhas não são iguais.'}
            )