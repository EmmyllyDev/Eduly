from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

# -----------------------------
# LOGIN
# -----------------------------
def login_eduly(request):
    if request.user.is_authenticated:
        # Se o usuário já está logado, redireciona para o home
        return redirect('usuarios:home_redirect')

    if request.method == 'POST':
        # Cria uma instância do formulário com os dados enviados
        form = AuthenticationForm(request, data=request.POST)
        
        # O Django valida o formulário (usuário existe, senha correta, usuário ativo)
        if form.is_valid():
            # Pega o usuário validado pelo formulário
            user = form.get_user()
            login(request, user)
            logger.info(f"Usuário '{user.username}' autenticado com sucesso.")
            
            # A view de login NÃO decide para onde o usuário vai.
            # Ela apenas redireciona para a view 'home_redirect', que tem essa responsabilidade.
            return redirect('usuarios:home_redirect')
        else:
            # Se o formulário for inválido, o próprio form já contém os erros.
            messages.error(request, 'Usuário ou senha inválidos. Tente novamente.')
            logger.warning(f"Tentativa de login falhou para o usuário '{request.POST.get('username')}'.")
    
    # Se a requisição for GET, apenas mostra o formulário de login vazio
    else:
        form = AuthenticationForm()

    return render(request, 'autenticacao/login.html', {'form': form})


# -----------------------------
# LOGOUT
# -----------------------------
def logout_eduly(request):
    logger.info(f"Usuário '{request.user.username}' fez logout.")
    logout(request)
    return render(request, 'autenticacao/logout.html') # Redireciona para a página de logout


# -----------------------------
# RECUPERAÇÃO DE SENHA (Apenas a exibição da página)
# -----------------------------
def recuperar_senha(request):
    logger.debug("Página de recuperação de senha acessada.")
    return render(request, 'autenticacao/recuperar-senha.html')


# -----------------------------
# REDIRECIONAMENTO DA RAIZ
# -----------------------------
def redirect_to_login(request):
    """View para a URL raiz ('') que apenas redireciona para a página de login."""
    return redirect('usuarios:login_eduly')