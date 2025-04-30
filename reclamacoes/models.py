from django.db import models
from django.contrib.auth.models import User

class Empresa(models.Model):
    nome = models.CharField(max_length=50)
    cnpj = models.CharField(max_length=14, unique=True)

    def __str__(self):
        return self.nome


class Reclamacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100) 
    descricao = models.TextField()            
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.titulo} - {self.empresa.nome}"
