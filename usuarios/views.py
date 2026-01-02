from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .forms import CadastroUsuarioForm
from django.contrib import messages
from django.contrib.auth import logout as django_logout
from django.contrib.auth import authenticate, login

def cadastro_view(request):
    if request.method == 'POST':
        request.session['cadastro_dados'] = request.POST
        return redirect('usuarios:concluir_cadastro')
    
    form = CadastroUsuarioForm()
    return render(request, 'pages/registro2.html', {'form': form})

def concluir_cadastro(request):
    dados = request.session.get('cadastro_dados')
    
    if not dados:
        messages.error(request, 'Nenhum dado de cadastro encontrado.')
        return redirect('usuarios:registro')
    
    form = CadastroUsuarioForm(dados)
    
    if form.is_valid():
        # Salva o usuário corretamente
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password']) 
        user.save()
        
        if 'cadastro_dados' in request.session:
            del request.session['cadastro_dados']
        
        messages.success(request, 'Usuário criado com sucesso! Faça login.')
        return redirect('reclamacoes:home')
    else:
        messages.error(request, 'Por favor, corrija os erros abaixo.')
        return render(request, 'pages/registro2.html', {'form': form})
    


def login_usuario(request):
    if request.user.is_authenticated:
        return redirect('reclamacoes:home')
    if request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('password')

        user = authenticate(request, username=username, password=senha)

        if user is not None:
            login(request, user)
            return redirect('reclamacoes:home') 
        else:
            return render(request, 'pages/login.html', {'erro': 'Usuário ou senha incorretos'})

    return render(request, 'pages/login.html')

def logout(request):
    django_logout(request)
    return redirect('reclamacoes:home')
