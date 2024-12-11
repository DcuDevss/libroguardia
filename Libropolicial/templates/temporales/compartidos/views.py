
#compartidos/views
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .forms import CustomLoginForm

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
            'divisioncomunicaciones': 'divisioncomunicaciones_list'
        }
        for group, url in user_group_redirects.items():
            if self.request.user.groups.filter(name=group).exists():
                return reverse_lazy(url)
        return reverse_lazy('no_permission')


    #def get_success_url(self):
    #    if self.request.user.groups.filter(name='comisariaprimera').exists():
     #       return reverse_lazy('comisaria_primera_list')
      #  elif self.request.user.groups.filter(name='comisariasegunda').exists():
       #     return reverse_lazy('comisaria_segunda_list')
       # elif self.request.user.groups.filter(name='divisioncomunicaciones').exists():
        #    return reverse_lazy('divisioncomunicaciones_list')
        #else:
         #   return reverse_lazy('no_permission')

from django.http import JsonResponse
from datetime import datetime

def check_message(request):
    # Definir las horas en las que debe aparecer el mensaje
    current_time = datetime.now().time()
    show_message = False

    # Condiciones para mostrar el mensaje
    if (current_time >= datetime.strptime('19:20', '%H:%M').time() and current_time <= datetime.strptime('19:22', '%H:%M').time()) or \
       (current_time >= datetime.strptime('21:20', '%H:%M').time() and current_time <= datetime.strptime('21:22', '%H:%M').time()) or \
       (current_time >= datetime.strptime('23:30', '%H:%M').time() and current_time <= datetime.strptime('23:32', '%H:%M').time()):
        show_message = True

    return JsonResponse({'show_message': show_message})


    ''''eesto va en archivo {% blocktrans 
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                function checkForMessage() {
                    fetch('/compartido/check-message/')
                        .then(response => response.json())
                        .then(data => {
                            if (data.show_message) {
                                const alertBox = document.getElementById('alert-box');
                                alertBox.classList.remove('hidden');
                                setTimeout(() => {
                                    alertBox.classList.add('hidden');
                                }, 120000); // 2 minutos (120,000 ms)
                            }
                        })
                        .catch(error => console.error('Error:', error));
                }
            
                // Ejecuta la función cada minuto
                setInterval(checkForMessage, 60000);
                // Ejecuta al cargar la página por primera vez
                checkForMessage();
            });
        </script>%}
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            function checkForMessage() {
                fetch('/compartido/check-message/')
                    .then(response => response.json())
                    .then(data => {
                        if (data.show_message) {
                            const alertBox = document.getElementById('alert-box');
                            alertBox.classList.remove('hidden');
                            setTimeout(() => {
                                alertBox.classList.add('hidden');
                            }, 120000); // 2 minutos (120,000 ms)
                        }
                    })
                    .catch(error => console.error('Error:', error));
            }
        
            // Ejecuta la función cada minuto
            setInterval(checkForMessage, 60000);
            // Ejecuta al cargar la página por primera vez
            checkForMessage();
        });
    </script>
    {% endblocktrans %}

    from django.http import JsonResponse
from datetime import datetime
from django.core.cache import cache

def check_message(request):
    # Intenta obtener el valor de la caché
    cached_response = cache.get('check_message_cache')
    
    if cached_response:
        # Si existe en caché, devuelve el resultado almacenado
        return JsonResponse(cached_response)

    # Si no está en caché, ejecuta la lógica para calcular el mensaje
    current_time = datetime.now().time()
    show_message = False

    # Condiciones para mostrar el mensaje
    if (current_time >= datetime.strptime('15:15', '%H:%M').time() and current_time <= datetime.strptime('15:17', '%H:%M').time()) or \
       (current_time >= datetime.strptime('15:32', '%H:%M').time() and current_time <= datetime.strptime('15:34', '%H:%M').time()) or \
       (current_time >= datetime.strptime('15:40', '%H:%M').time() and current_time <= datetime.strptime('15:43', '%H:%M').time()):
        show_message = True

    # Almacena el resultado en la caché durante 30 segundos
    response_data = {'show_message': show_message}
    cache.set('check_message_cache', response_data, 30)

    return JsonResponse(response_data)
