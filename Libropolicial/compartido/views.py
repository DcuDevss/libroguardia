from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .forms import CustomLoginForm, AsignarPermisoForm
from .models import CargaDatosPermiso
from django.contrib.auth.decorators import login_required, user_passes_test

# Vista de sin permiso
def no_permission(request):
    return render(request, 'no_permission.html', {})

# Vista de la página de inicio
class HomeView(TemplateView):
    template_name = 'home.html'

class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = CustomLoginForm

    def get_success_url(self):
        user_group_redirects = {
            'jefesdeturno': 'home_opciones',
            'jefessuperiores': 'home_opciones',
            'oficialesservicios': 'home_opciones',
            'comisariaprimera': 'comisaria_primera_list',
            'comisariasegunda': 'comisaria_segunda_list',
            'comisaria_primeraRG': 'comisariaprimeraRG_list',
            'comisaria_segundaRG': 'comisariasegundaRG_list',
            'comisaria_terceraRG': 'comisariaterceraRG_list',
            'comisaria_cuartaRG': 'comisariacuartaRG_list',
            'comisaria_quintaRG': 'comisariaquintaRG_list',
            'divisioncomunicaciones': 'divisioncomunicaciones_list'
        }

        # Verificar si el usuario es superusuario
        if self.request.user.is_superuser:
            return reverse_lazy('home_opciones')  # Redirigir al home de opciones si es superusuario

        # Comprobar si el usuario tiene permisos asignados
        for group, url in user_group_redirects.items():
            if self.request.user.groups.filter(name=group).exists():
                # Si no tiene permisos asignados, redirigir a asignar permisos
                if not CargaDatosPermiso.objects.filter(usuario=self.request.user).exists():
                    return reverse_lazy('asignar_permiso')
                # Si tiene permisos asignados, redirigir a la vista correspondiente de su grupo
                return reverse_lazy(url)

        # Si no es un grupo válido, redirigir a no_permission
        return reverse_lazy('no_permission')

# Función para verificar si el usuario tiene rol de asignar permisos
def tiene_rol_de_permiso(usuario):
    roles_validos = ['jefesdeturno', 'jefessuperiores', 'oficialesservicios']
    return usuario.groups.filter(name__in=roles_validos).exists()

# Vista para asignar permisos
@login_required
@user_passes_test(tiene_rol_de_permiso)
def asignar_permiso(request):
    if request.method == 'POST':
        form = AsignarPermisoForm(request.POST)
        if form.is_valid():
            form.save()  # Guardar los permisos en la base de datos
            return redirect('vista_permisos')  # Redirigir a una vista de confirmación o lista de permisos
    else:
        form = AsignarPermisoForm()

    return render(request, 'asignar_permiso.html', {'form': form})

# Vista para listar los permisos asignados
@login_required
@user_passes_test(tiene_rol_de_permiso)
def vista_permisos(request):
    permisos = CargaDatosPermiso.objects.all()
    return render(request, 'vista_permisos.html', {'permisos': permisos})


# Vista de opciones de inicio
@login_required
def home_opciones(request):
    # Si el usuario pertenece a los grupos que pueden asignar permisos
    if request.user.groups.filter(name__in=['jefesdeturno', 'jefessuperiores', 'oficialesservicios']).exists():
        return render(request, 'home_opciones.html', {'group': 'asignar_permiso'})

    # Si el usuario tiene permisos asignados, mostrar opciones de carga de datos
    if CargaDatosPermiso.objects.filter(usuario=request.user).exists():
        return render(request, 'home_opciones.html', {'group': 'usuario_con_permiso'})

    # Si no tiene permisos asignados, mostrar la opción de asignar permisos
    return render(request, 'home_opciones.html', {'group': 'sin_permiso'})
