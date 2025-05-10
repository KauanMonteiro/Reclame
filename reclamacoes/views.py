from django.shortcuts import get_object_or_404, redirect, render
from .models import Empresa,Reclamacao,Denuncia
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import logout as django_logout


def home(request):
    empresa = Empresa.objects.all().filter(aprovar=True,rejeitar = False)
    return render(request,'pages/home.html',{'empresa':empresa})


def ver_mais_empresa(request,empresa_id):
    empresa = get_object_or_404(Empresa,pk=empresa_id)
    reclamacoes = Reclamacao.objects.filter(empresa=empresa).order_by('-criado_em').filter(bloquear=False)
    return render(request, 'pages/ver_mais_empresa.html', {'empresa': empresa,'reclamacoes': reclamacoes})


@login_required(login_url='/login/')
def cadastrar_empresa(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cnpj = request.POST.get('cnpj')

        empresa = Empresa.objects.create(nome=nome,cnpj=cnpj)

        return redirect('home')
    return render(request,'pages/cadastro_empresa.html')


def ver_mais_reclamacao(request,reclamacao_id):
    reclamacao = get_object_or_404(Reclamacao,pk=reclamacao_id)
    return render(request,'pages/ver_mais_reclamacao.html',{'reclamacao':reclamacao})

@login_required(login_url='/login/')
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

@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def area_admin(request):
    reclamacoes_denuncias = Reclamacao.objects.filter(bloquear=False).order_by('-denuncias_count')
    reclamacoes = Reclamacao.objects.filter(bloquear=True).order_by('-denuncias_count')
    empresas = Empresa.objects.filter(aprovar=False)
    empresas_aprovadas = Empresa.objects.filter(aprovar=True, rejeitar=False)
    empresas_rejeitadas = Empresa.objects.filter(rejeitar=True)

    return render(request,'pages/adminpage.html',{'reclamacoes_denuncias': reclamacoes_denuncias,'reclamacoes': reclamacoes,'empresas': empresas,'empresas_aprovadas': empresas_aprovadas,'empresas_rejeitadas': empresas_rejeitadas})


def denunciar(request,reclamacao_id):
    reclamacao = get_object_or_404(Reclamacao,pk=reclamacao_id)

    if request.method == "POST":
         motivo = request.POST.get('motivo')
         comentario= request.POST.get('comentario')
         Denuncia.objects.create(
             usuario = request.user,
             reclamacao = reclamacao,
             motivo = motivo,
             comentario = comentario,
         )
         reclamacao.denuncias_count += 1
         reclamacao.save()
         return redirect(home)

    return render(request,'pages/denunciar.html')


def bloquear(request,reclamacao_id):
    reclamacao = get_object_or_404(Reclamacao,pk=reclamacao_id)

    if request.method=='POST':
        reclamacao.bloquear = True
        reclamacao.save()

    return redirect(area_admin)



def desbloquear(request,reclamacao_id):
    reclamacao = get_object_or_404(Reclamacao,pk=reclamacao_id)

    if request.method=='POST':
        reclamacao.bloquear = False
        reclamacao.save()

    return redirect(area_admin)


def aprovar(request,empresa_id):
    empresa = get_object_or_404(Empresa,pk=empresa_id)

    if request.method=='POST':
        empresa.aprovar = True
        empresa.rejeitar = False
        empresa.save()

    return redirect(area_admin)


def rejeitar(request,empresa_id):
    empresa = get_object_or_404(Empresa,pk=empresa_id)

    if request.method=='POST':
        empresa.aprovar = None
        empresa.rejeitar = True
        empresa.save()

    return redirect(area_admin)


def cadastro_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'registro.html', {'erro': 'Usuário já existe!'})

        user = User.objects.create_user(username=username, password=senha, email=email)
        user.save()

        return redirect(login_usuario)

    return render(request, 'pages/registro.html')

def login_usuario(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('password')

        user = authenticate(request, username=username, password=senha)

        if user is not None:
            login(request, user)
            return redirect(home) 
        else:
            return render(request, 'pages/login.html', {'erro': 'Usuário ou senha incorretos'})

    return render(request, 'pages/login.html')

def logout(request):
    django_logout(request)
    return redirect(home)
