from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render
import logging
from django.contrib import messages

# Configuração do logger
logger = logging.getLogger(__name__)

def is_administrador(user):
    """Verifica se o usuário é autenticado e tem o perfil de Administrador."""
    return user.is_authenticated and user.perfil_acesso == 'Administrador'

def is_professor(user):
    """Verifica se o usuário é autenticado e tem o perfil de Professor."""
    return user.is_authenticated and user.perfil_acesso == 'Professor'

def is_aluno(user):
    """Verifica se o usuário é autenticado e tem o perfil de Aluno."""
    return user.is_authenticated and user.perfil_acesso == 'Aluno'


'''
--------------------------------------------------------------------------------
    REDIRECIONAMENTO PÓS-LOGIN E DASHBOARDS
--------------------------------------------------------------------------------
'''

@login_required(login_url='usuarios:login_eduly')
def home_redirect(request):
    """
    Redireciona o usuário para o dashboard apropriado após o login,
    com base no seu campo 'perfil_acesso'.
    """
    papel = request.user.perfil_acesso
    
    if papel:
        logger.info(f"Usuário '{request.user.username}' com papel '{papel}' acessou o redirecionador.")
        
        if papel == 'Administrador':
            return redirect('usuarios:dashboard_administrador')
        elif papel == 'Professor':
            return redirect('usuarios:dashboard_professor')
        elif papel == 'Aluno':
            return redirect('usuarios:dashboard_aluno')
        else:
            logger.warning(f"Usuário '{request.user.username}' com papel desconhecido '{papel}'.")
            return redirect('usuarios:login_eduly')
    else:
        logger.error(f"Usuário '{request.user.username}' não possui um perfil_acesso definido.")
        messages.error(request, 'Sua conta não tem um perfil configurado. Contate o suporte.')

        return redirect('usuarios:login_eduly')


@user_passes_test(is_administrador, login_url='usuarios:login_eduly')
def dashboard_administrador(request):
    """
    Exibe o painel principal para usuários com o papel de Administrador.
    """
    logger.info(f"Dashboard do administrador acessado por '{request.user.username}'.")
    context = {
        'usuario': request.user
        }
    return render(request, 'usuarios/administrador/dashboard_administrador.html', context)


@user_passes_test(is_professor, login_url='usuarios:login_eduly')
def dashboard_professor(request):
    """
    Exibe o painel principal para usuários com o papel de Professor.
    """
    logger.info(f"Dashboard do professor acessado por '{request.user.username}'.")
    context = {
        'usuario': request.user
        }
    return render(request, 'usuarios/professor/dashboard_professor.html', context)


@user_passes_test(is_aluno, login_url='usuarios:login_eduly')
def dashboard_aluno(request):
    """
    Exibe o painel principal para usuários com o papel de Aluno.
    """
    logger.info(f"Dashboard do aluno acessado por '{request.user.username}'.")
    context = {
        'usuario': request.user
        }
    return render(request, 'usuarios/aluno/dashboard_aluno.html', context)