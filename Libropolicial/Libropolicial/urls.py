from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

# Define las rutas (URL patterns) principales para el proyecto
urlpatterns = [
    # Ruta para la interfaz de administración de Django
    path('admin/', admin.site.urls),

    # Incluye las rutas definidas en 'compartido.urls'
    path('', include('compartido.urls')),

    # Incluye las rutas definidas en 'comisarias.urls'cambios
    path('comisarias/', include('comisarias.urls')),

    # Incluye las rutas definidas en 'comisariasriogrande.urls'
    path('comisariasriogrande/', include('comisariasriogrande.urls')),

    
    # Incluye las rutas definidas en 'comisariastolhuin.urls'
    path('comisariastolhuin/', include('comisariastolhuin.urls')),
    
    # Incluye las rutas definidas en 'divisioncomunicaciones.urls'
    path('divisioncomunicaciones/', include('divisioncomunicaciones.urls')),  


    # Puedes incluir otras aplicaciones de la misma manera
]

# Configuración para servir archivos cargados por los usuarios
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
