# Importa MiddlewareMixin para crear middlewares compatibles con versiones anteriores de Django
from django.utils.deprecation import MiddlewareMixin
# Importa redirect para redirigir a los usuarios a una URL específica
from django.shortcuts import redirect
# Importa timezone para trabajar con fechas y horas conscientes de la zona horaria
from django.utils import timezone
# Importa timedelta para trabajar con diferencias de tiempo
from datetime import timedelta


class NoCacheMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Deshabilita la caché en los navegadores
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response


# Middleware que redirige a los usuarios autenticados a sus vistas específicas según su grupo
class RedirectAuthenticatedUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Define las URLs restringidas donde no deben estar los usuarios autenticados
        restricted_urls = ['/', '/login/', '/no-permission/']
        if request.user.is_authenticated and request.path in restricted_urls:
            # Redirige a los usuarios basados en su grupo
            if request.user.groups.filter(name='comisariaprimera').exists():
                return redirect('comisaria_primera_list')
            elif request.user.groups.filter(name='comisariasegunda').exists():
                return redirect('comisaria_segunda_list')
            elif request.user.groups.filter(name='comisariatercera').exists():
                return redirect('comisaria_tercera_list')
            elif request.user.groups.filter(name='comisariacuarta').exists():
                return redirect('comisaria_cuarta_list')
            elif request.user.groups.filter(name='comisariaquinta').exists():
                return redirect('comisaria_quinta_list')
            elif request.user.groups.filter(name='comisariaprimeraRG').exists():
                return redirect('comisaria_primeraRG_list')
            elif request.user.groups.filter(name='comisariasegundaRG').exists():
                return redirect('comisaria_segundaRG_list')
            elif request.user.groups.filter(name='comisariaterceraRG').exists():
                return redirect('comisaria_terceraRG_list')
            elif request.user.groups.filter(name='comisariacuartaRG').exists():
                return redirect('comisaria_cuartaRG_list') 
            elif request.user.groups.filter(name='comisariaquintaRG').exists():
                return redirect('comisaria_quintaRG_list')
            elif request.user.groups.filter(name='divisioncomunicaciones').exists():
                return redirect('divisioncomunicaciones_list')
            elif request.user.groups.filter(name='estadisticas').exists():
                return redirect('estadisticas_comisarias')
            else:
                return redirect('no_permission')
        return None


# Middleware que cierra la sesión de los usuarios después de un período de inactividad
class InactivityLogoutMiddleware(MiddlewareMixin):
    # Método que procesa la solicitud para comprobar la actividad del usuario
    def process_request(self, request):
        # Comprueba si el usuario está autenticado
        if request.user.is_authenticated:
            # Obtiene la última actividad del usuario desde la sesión
            last_activity = request.session.get('last_activity')
            if last_activity:
                # Convierte la última actividad en un objeto datetime
                last_activity = timezone.datetime.fromisoformat(last_activity)
                # Comprueba si el tiempo transcurrido desde la última actividad es mayor que una hora
                if timezone.now() - last_activity > timedelta(hours=1):
                    # Importa logout para cerrar la sesión del usuario
                    from django.contrib.auth import logout
                    # Cierra la sesión del usuario
                    logout(request)
                    # Redirige al usuario a la página de inicio de sesión
                    return redirect('login')
            # Actualiza la última actividad del usuario en la sesión con la hora actual
            request.session['last_activity'] = timezone.now().isoformat()
