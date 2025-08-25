from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404, render, redirect
import logging

from django.urls import reverse

from apps.usuarios.models import Usuario

User = get_user_model()

logger = logging.getLogger(__name__)


@login_required(login_url='usuarios:login_eduly')
def perfil_usuario(request):
    """
    Exibe a página principal do perfil do usuário logado.
    """
    logger.info(f"Usuário '{request.user.username}' acessou a página de perfil.")
    context = {
        'usuario': request.user
    }
    return render(request, 'autenticacao/perfil-usuario.html', context)


@login_required(login_url='usuarios:login_eduly')
def editar_perfil_usuario(request):
    """
    Processa a atualização das informações básicas do perfil (nome e e-mail).
    """
    if request.method == 'POST':
        user = request.user
        nome = request.POST.get('first_name', user.first_name)
        sobrenome = request.POST.get('last_name', user.last_name)
        email = request.POST.get('email', user.email)

        if User.objects.exclude(pk=user.pk).filter(email__iexact=email).exists():
            logger.warning(f"Usuário '{user.username}' tentou alterar para um e-mail já existente: {email}")
            messages.error(request, 'Já existe um usuário cadastrado com este e-mail.')
            return redirect('usuarios:perfil_usuario')

        user.first_name = nome
        user.last_name = sobrenome
        user.email = email
        user.save()

        logger.info(f"Usuário '{user.username}' atualizou seu perfil (nome/email).")
        messages.success(request, 'Seu perfil foi atualizado com sucesso!')
        
    return redirect('usuarios:perfil_usuario')


@login_required(login_url='usuarios:login_eduly')
def alterar_senha_usuario(request):
    """
    Processa a alteração de senha do usuário.
    """
    if request.method == 'POST':
        user = request.user
        senha_atual = request.POST.get('senha_atual')
        nova_senha = request.POST.get('nova_senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        # 1. Valida a senha atual
        if not check_password(senha_atual, user.password):
            logger.warning(f"Usuário '{user.username}' forneceu senha atual incorreta.")
            messages.error(request, 'Sua senha atual está incorreta. Tente novamente.')
            return redirect('usuarios:perfil_usuario')

        # 2. Valida se a nova senha e a confirmação são iguais
        if nova_senha != confirmar_senha:
            logger.warning(f"Usuário '{user.username}' não coincidiu a confirmação de senha.")
            messages.error(request, 'A nova senha e a confirmação não coincidem.')
            return redirect('usuarios:perfil_usuario')

        # 3. Valida o comprimento mínimo da nova senha
        if len(nova_senha) < 8:
            logger.warning(f"Usuário '{user.username}' tentou usar uma senha muito curta.")
            messages.warning(request, 'A nova senha deve ter pelo menos 8 caracteres.')
            return redirect('usuarios:perfil_usuario')

        # 4. Salva a nova senha e atualiza a sessão
        user.set_password(nova_senha)
        user.save()
        
        # Mantém o usuário logado após a mudança de senha.
        update_session_auth_hash(request, user)
        
        logger.info(f"Usuário '{user.username}' alterou a senha com sucesso.")
        messages.success(request, 'Sua senha foi alterada com sucesso!')

    return redirect('usuarios:perfil_usuario')

def is_admin(user):
    return user.is_authenticated and user.perfil_acesso == 'Administrador'

@login_required(login_url='usuarios:login_eduly')
@user_passes_test(is_admin, login_url='usuarios:home_redirect') # Garante que só admins acessem
def gerenciar_usuarios(request):
    """
    Exibe uma lista de usuários filtrada por tipo (aluno, professor, etc.)
    e permite o gerenciamento básico.
    """
    tipo_usuario = request.GET.get('tipo', 'aluno')

    if tipo_usuario not in ['aluno', 'professor', 'administrador']:
        tipo_usuario = 'aluno' 

    usuarios_filtrados = User.objects.filter(perfil_acesso=tipo_usuario.title())

    context = {
        'usuarios': usuarios_filtrados,
        'tipo_usuario': tipo_usuario,
        'active_page': 'usuarios' 
    }
    
    return render(request, 'usuarios/gerenciar_usuarios.html', context)

@user_passes_test(is_admin, login_url="usuarios:login_eduly")
def excluir_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)

    if request.method == "POST":
        usuario.delete()
        messages.success(request, "Usuário excluído com sucesso!")
        return redirect(reverse("usuarios:gerenciar_usuarios") + f"?tipo={usuario.perfil_acesso.lower()}")

    return render(request, "autenticacao/confirmar_exclusao.html", {"usuario": usuario})

@login_required
@user_passes_test(is_admin, login_url='usuarios:home_redirect')
def inativar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    usuario.is_active = False
    usuario.save()
    messages.success(request, f"O usuário {usuario.username} foi inativado com sucesso.")
    return redirect('usuarios:gerenciar_usuarios')

@login_required
@user_passes_test(is_admin, login_url='usuarios:home_redirect')
def reativar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    usuario.is_active = True
    usuario.save()
    messages.success(request, f"Usuário {usuario.username} foi reativado.")
    return redirect("usuarios:gerenciar_usuarios")

@login_required(login_url='usuarios:login_eduly')
@user_passes_test(is_admin, login_url='usuarios:home_redirect')
def editar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        usuario.first_name = request.POST.get("first_name", usuario.first_name)
        usuario.last_name = request.POST.get("last_name", usuario.last_name)
        usuario.email = request.POST.get("email", usuario.email)
        usuario.perfil_acesso = request.POST.get("perfil_acesso", usuario.perfil_acesso)
        usuario.save()
        messages.success(request, f"Usuário {usuario.username} atualizado com sucesso!")
        return redirect("usuarios:gerenciar_usuarios")

    return render(request, "autenticacao/editar_usuario.html", {"usuario": usuario})