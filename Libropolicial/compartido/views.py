#compartidos/views
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .forms import CustomLoginForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy


def no_permission(request):
    return render(request, 'no_permission.html', {})

class HomeView(TemplateView):
    template_name = 'home.html'

class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = CustomLoginForm

    def get_success_url(self):
        user_group_redirects = {
            'comisariaprimera': 'comisaria_primera_list',
            'comisariasegunda': 'comisaria_segunda_list',
            'comisaria_primeraRG': 'comisariaprimeraRG_list',
            'comisaria_segundaRG': 'comisariasegundaRG_list',
            'comisaria_terceraRG': 'comisariaterceraRG_list',
            'comisaria_cuartaRG': 'comisariacuartaRG_list',
            'comisaria_quintaRG': 'comisariaquintaRG_list',
            'divisioncomunicaciones': 'divisioncomunicaciones_list'
        }
        for group, url in user_group_redirects.items():
            if self.request.user.groups.filter(name=group).exists():
                return reverse_lazy(url)
        return reverse_lazy('no_permission')


@login_required
def perfil_usuario(request):
    return render(request, 'perfil_usuario.html', {'user': request.user})

@csrf_exempt
@login_required
def cambiar_contrasena(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Importante para mantener la sesión
            return JsonResponse({'success': True})
        else:
            # Envía los errores específicos al cliente
            errors = {field: error.get_json_data() for field, error in form.errors.items()}
            return JsonResponse({'success': False, 'errors': errors})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

class CustomPasswordResetView(PasswordResetView):
    email_template_name = "registration/password_reset_email.html"
    subject_template_name = "registration/custom_password_reset_subject.txt"
    html_email_template_name = "registration/password_reset_email.html"
    success_url = reverse_lazy("registration/password_reset_done")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["protocol"] = "https" if self.request.is_secure() else "http"
        context["domain"] = self.request.get_host()
        return context
