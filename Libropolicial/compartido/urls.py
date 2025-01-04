# compartido/urls.py
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import HomeView, CustomLoginView, no_permission, perfil_usuario,cambiar_contrasena, CustomPasswordResetView   #check_message
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('no-permission/', no_permission, name='no_permission'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  # Añadido el LogoutView
   # path('check-message/', check_message, name='check_message'),

    # rutas el cambio de contraseña desde la vista de perfil
    path('perfil/', perfil_usuario, name='perfil_usuario'),
    path('password_change/', cambiar_contrasena, name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),

    # rutas el reestablecimiento de contraseña
    path('password_reset/', CustomPasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    
]
