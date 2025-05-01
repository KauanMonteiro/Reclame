from django.shortcuts import get_object_or_404, redirect, render
from .models import Empresa,Reclamacao

def home(request):
    empresa = Empresa.objects.all()
    return render(request,'pages/home.html',{'empresa':empresa})


def ver_mais_empresa(request,empresa_id):
    empresa = get_object_or_404(Empresa,pk=empresa_id)
    reclamacoes = Reclamacao.objects.filter(empresa=empresa).order_by('-criado_em')
    return render(request, 'pages/ver_mais_empresa.html', {'empresa': empresa,'reclamacoes': reclamacoes})

def cadastrar_empresa(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cnpj = request.POST.get('cnpj')

        empresa = Empresa.objects.create(nome=nome,cnpj=cnpj)

        return redirect('home')
    return render(request,'pages/cadastro_empresa.html')



def criar_reclamacao(request, empresa_id):
    empresa = get_object_or_404(Empresa, pk=empresa_id)

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')

        Reclamacao.objects.create(
            usuario=request.user,
            empresa=empresa,
            titulo=titulo,
            descricao=descricao
        )
        return redirect('home')

    return render(request, 'pages/criar_reclamacao.html', {'empresa': empresa})
