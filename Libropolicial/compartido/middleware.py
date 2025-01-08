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

from django.contrib.auth import logout
# Middleware que cierra la sesión de los usuarios después de un período de inactividad
class InactivityLogoutMiddleware(MiddlewareMixin):
    """
    Middleware para cerrar la sesión de los usuarios después de un período de inactividad
    y gestionar el estado 'is_online' de cada usuario.
    """

    def process_request(self, request):
        # Si el usuario está autenticado
        if request.user.is_authenticated:
            # Obtener o crear el perfil personal asociado al usuario
            personal_profile = request.user.personal_profile

            # Establecer el usuario como conectado si no está marcado como 'online'
            if not personal_profile.is_online:
                personal_profile.is_online = True
                personal_profile.save()

            # Comprobar la última actividad registrada en la sesión
            last_activity = request.session.get('last_activity')
            if last_activity:
                # Convertir la última actividad en un objeto datetime
                last_activity = timezone.datetime.fromisoformat(last_activity)
                # Comprobar si ha pasado más de una hora desde la última actividad
                if timezone.now() - last_activity > timedelta(hours=1):
                    # Marcar al usuario como desconectado
                    personal_profile.is_online = False
                    personal_profile.save()
                    # Cerrar la sesión del usuario
                    logout(request)
                    return redirect('login')

            # Actualizar la última actividad en la sesión
            request.session['last_activity'] = timezone.now().isoformat()

        # Si el usuario no está autenticado pero tiene un perfil asociado
        elif hasattr(request.user, 'personal_profile'):
            personal_profile = request.user.personal_profile
            if personal_profile.is_online:
                # Marcar al usuario como desconectado
                personal_profile.is_online = False
                personal_profile.save()
