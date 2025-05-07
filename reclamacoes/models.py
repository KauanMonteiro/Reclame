from django.db import models
from django.contrib.auth.models import User

class Empresa(models.Model):
    nome = models.CharField(max_length=50)
    cnpj = models.CharField(max_length=14, unique=True)
    aprovar = models.BooleanField(default=False,blank=True, null= True)
    rejeitar = models.BooleanField(blank=True, null= True)
    def __str__(self):
        return self.nome


class Reclamacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100) 
    descricao = models.TextField()            
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    denuncias_count = models.PositiveIntegerField(default=0)
    bloquear = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.titulo} - {self.empresa.nome}"

class Denuncia(models.Model):
    MOTIVOS = [
        ('SPAM', 'Conteúdo inadequado'),
        ('OFENSIVO', 'Linguagem ofensiva'),
        ('FALSO', 'Informação falsa'),
        ('OUTRO', 'Outro motivo'),
    ]

    reclamacao = models.ForeignKey(Reclamacao, on_delete=models.CASCADE, related_name='denuncias')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL,null= True) 
    motivo = models.CharField(max_length=20, choices=MOTIVOS)
    comentario = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Denúncia por {self.usuario} em {self.reclamacao.titulo}"