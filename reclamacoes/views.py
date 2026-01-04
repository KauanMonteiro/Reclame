from django.shortcuts import get_object_or_404, redirect, render
from .models import Empresa,Reclamacao,Denuncia
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,user_passes_test
from .forms import EmpresaForm, ReclamacaoForm,DenunciaForm
from django.contrib import messages

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
        form = EmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empresa cadastrada com sucesso! Aguarde a aprovação.')
            return redirect('reclamacoes:home')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
            return render(request,'pages/cadastro_empresa.html',{'form':form})
    else:
        form = EmpresaForm()
    return render(request,'pages/cadastro_empresa.html',{'form':form})


def ver_mais_reclamacao(request,reclamacao_id):
    reclamacao = get_object_or_404(Reclamacao,pk=reclamacao_id)
    return render(request,'pages/ver_mais_reclamacao.html',{'reclamacao':reclamacao})

@login_required(login_url='/login/')
def criar_reclamacao(request, empresa_id):
    empresa = get_object_or_404(Empresa, pk=empresa_id)
    if request.method == 'POST':
        form = ReclamacaoForm(request.POST)
        if form.is_valid():
            reclamacao = form.save(commit=False)
            reclamacao.empresa = empresa
            reclamacao.usuario = request.user
            reclamacao.save()
            messages.success(request,'Reclamação realizada com sucesso!')
        else:
            messages.error(request,'Por favor, corrija os erros abaixo.')
            return render(request, 'pages/criar_reclamacao.html', {'form': form, 'empresa':empresa})
    else:
        form =ReclamacaoForm()

    return render(request, 'pages/criar_reclamacao.html', {'form': form, 'empresa':empresa})

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
        form = DenunciaForm(request.POST)
        if form.is_valid():
            denuncia = form.save(commit=False)
            denuncia.usuario = request.user
            denuncia.reclamacao = reclamacao
            denuncia.save()

            reclamacao.denuncias_count += 1
            reclamacao.save()
            return redirect('reclamacoes:home')
    else:
        form = DenunciaForm()

    return render(request,'pages/denunciar.html',{'form':form,'reclamacao':reclamacao})


def bloquear(request,reclamacao_id):
    reclamacao = get_object_or_404(Reclamacao,pk=reclamacao_id)

    if request.method=='POST':
        reclamacao.bloquear = True
        reclamacao.save()

    return redirect('reclamacoes:area_admin')



def desbloquear(request,reclamacao_id):
    reclamacao = get_object_or_404(Reclamacao,pk=reclamacao_id)

    if request.method=='POST':
        reclamacao.bloquear = False
        reclamacao.save()

    return redirect('reclamacoes:area_admin')


def aprovar(request,empresa_id):
    empresa = get_object_or_404(Empresa,pk=empresa_id)

    if request.method=='POST':
        empresa.aprovar = True
        empresa.rejeitar = False
        empresa.save()

    return redirect('reclamacoes:area_admin')


def rejeitar(request,empresa_id):
    empresa = get_object_or_404(Empresa,pk=empresa_id)

    if request.method=='POST':
        empresa.aprovar = None
        empresa.rejeitar = True
        empresa.save()

    return redirect('reclamacoes:area_admin')

def ler_denuncias(request, reclamacao_id):
    denuncias = Denuncia.objects.all().order_by('-criado_em')
    reclamacao = get_object_or_404(Reclamacao,pk=reclamacao_id)
    empresa = get_object_or_404(Empresa,pk=reclamacao.empresa.id)
    return render(request,'pages/ler_denuncias.html',{'denuncias':denuncias,'reclamacao':reclamacao,'empresa':empresa})

def deletar_denuncia(request, denuncia_id):
    denuncia = get_object_or_404(Denuncia,pk=denuncia_id)
    reclamacao = get_object_or_404(Reclamacao,pk=denuncia.reclamacao.id)

    if request.method=='POST':
        reclamacao.denuncias_count -= 1
        reclamacao.save()
        denuncia.delete()

    return redirect('reclamacoes:ler_denuncias', reclamacao.id)