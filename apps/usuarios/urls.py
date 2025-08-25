from django.urls import path
from .views import views_auth, views_dashboard, views_perfil

app_name = "usuarios"  

urlpatterns = [
    path('', views_auth.redirect_to_login, name='home'), 
    path('login/', views_auth.login_eduly, name='login_eduly'),
    path('logout/', views_auth.logout_eduly, name='logout_eduly'),
    path('recuperar-senha/', views_auth.recuperar_senha, name='recuperar-senha'),

    path('home-redirect/', views_dashboard.home_redirect, name='home_redirect'),

    path('dashboard/administrador/', views_dashboard.dashboard_administrador, name='dashboard_administrador'),
    path('dashboard/professor/', views_dashboard.dashboard_professor, name='dashboard_professor'),
    path('dashboard/aluno/', views_dashboard.dashboard_aluno, name='dashboard_aluno'),

    path('perfil/', views_perfil.perfil_usuario, name='perfil_usuario'),
    path('perfil/editar/', views_perfil.editar_perfil_usuario, name='editar_perfil_usuario'),
    path('perfil/alterar-senha/', views_perfil.alterar_senha_usuario, name='alterar_senha_usuario'),

    path('gerenciar/', views_perfil.gerenciar_usuarios, name='gerenciar_usuarios'),
    path('usuario/editar/<int:user_id>/', views_perfil.editar_usuario, name='editar_usuario'),
    path('usuario/inativar/<int:user_id>/', views_perfil.inativar_usuario, name='inativar_usuario'),
    path('usuario/reativar/<int:user_id>/', views_perfil.reativar_usuario, name='reativar_usuario'),
    path('usuario/excluir/<int:pk>/', views_perfil.excluir_usuario, name='excluir_usuario'),
]