from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .forms import CadastroUsuarioForm
from django.contrib import messages

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