import os
import json
import mimetypes
from datetime import datetime, timedelta
from io import BytesIO

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import Q
from django.http import JsonResponse, HttpResponse, HttpRequest, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string, get_template
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView,DetailView, TemplateView

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

from xhtml2pdf import pisa

from Libropolicial.settings import MEDIA_ROOT
from .forms import ComisariaPrimeraForm, ComisariaSegundaForm, ComisariaTerceraForm, ComisariaCuartaForm, ComisariaQuintaForm, CustomLoginForm
from .models import ComisariaPrimera, ComisariaSegunda, ComisariaTercera, ComisariaCuarta, ComisariaQuinta, DependenciasSecundarias, CodigoPolicialUSH, DetalleDependenciaSecundaria, DetalleInstitucionFederal, DetalleServicioEmergencia, DetalleInstitucionHospitalaria, DetalleDependenciaMunicipal, DetalleDependenciaProvincial 
from compartido.models import UploadedPDF

from compartido.utils import user_is_in_group
import base64


#------------------funcion par de realizar las firmas--------------------------------------------

@login_required
def sign_comisaria_primera(request, pk):
    # Obtiene la instancia de ComisariaPrimera correspondiente al ID (pk) proporcionado.
    # Si no se encuentra, lanza una excepción 404.
    comisaria = get_object_or_404(ComisariaPrimera, pk=pk)
    
    # Obtiene el nombre completo del usuario actual, o su nombre de usuario si el nombre completo no está disponible.
    user_full_name = request.user.get_full_name() or request.user.username
    
    # Verifica si ya hay firmas en la instancia de ComisariaPrimera.
    if comisaria.firmas:
        # Si ya existen firmas, añade la firma del usuario actual, separada por una coma.
        comisaria.firmas += f", {user_full_name}"
    else:
        # Si no hay firmas previas, establece la firma del usuario actual como la primera firma.
        comisaria.firmas = user_full_name
    
    # Guarda los cambios en la instancia de ComisariaPrimera, pero solo actualiza el campo 'firmas'.
    comisaria.save(update_fields=['firmas'])  # Solo actualiza el campo firmas
    
    # Redirige al usuario a la vista de la lista de ComisariaPrimera después de firmar.
    return redirect(reverse('comisaria_primera_list'))
#-------------------------------------------------------------------------------------------------------

# Función para firmar en Comisaria Segunda
@login_required
def sign_comisaria_segunda(request, pk):
    comisaria = get_object_or_404(ComisariaSegunda, pk=pk)
    user_full_name = request.user.get_full_name() or request.user.username
    if comisaria.firmas:
        comisaria.firmas += f", {user_full_name}"
    else:
        comisaria.firmas = user_full_name
    comisaria.save(update_fields=['firmas'])  # Solo actualiza el campo firmas
    return redirect(reverse('comisaria_segunda_list'))

#---------------------------------------------------------------------------------------------------------

# Función para firmar en Comisaria Tercera
@login_required
def sign_comisaria_tercera(request, pk):
    comisaria = get_object_or_404(ComisariaTercera, pk=pk)
    user_full_name = request.user.get_full_name() or request.user.username
    if comisaria.firmas:
        comisaria.firmas += f", {user_full_name}"
    else:
        comisaria.firmas = user_full_name
    comisaria.save(update_fields=['firmas'])  # Solo actualiza el campo firmas
    return redirect(reverse('comisaria_tercera_list'))

#-------------------------------------------------------------------------------------------------

# Función para firmar en Comisaria Cuarta
@login_required
def sign_comisaria_cuarta(request, pk):
    comisaria = get_object_or_404(ComisariaCuarta, pk=pk)
    user_full_name = request.user.get_full_name() or request.user.username
    if comisaria.firmas:
        comisaria.firmas += f", {user_full_name}"
    else:
        comisaria.firmas = user_full_name
    comisaria.save(update_fields=['firmas'])  # Solo actualiza el campo firmas
    return redirect(reverse('comisaria_cuarta_list'))

#--------------------------------------------------------------------------------------------

# Función para firmar en Comisaria Quinta
@login_required
def sign_comisaria_quinta(request, pk):
    comisaria = get_object_or_404(ComisariaQuinta, pk=pk)
    user_full_name = request.user.get_full_name() or request.user.username
    if comisaria.firmas:
        comisaria.firmas += f", {user_full_name}"
    else:
        comisaria.firmas = user_full_name
    comisaria.save(update_fields=['firmas'])  # Solo actualiza el campo firmas
    return redirect(reverse('comisaria_quinta_list'))

#-------------------clase para ver la tabla los codigos -------------------------------------------------------------------------

# views.py

class ComisariaPrimeraListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    # Especifica el modelo de datos que se va a listar.
    model = ComisariaPrimera
    
    # Define la plantilla que se utilizará para renderizar la lista.
    template_name = 'comisarias/primera/comisaria_primera_list.html'
    
    # Define el nombre del contexto que contendrá la lista de registros.
    context_object_name = 'records'

    # Método que determina si el usuario tiene permiso para acceder a esta vista.
    def test_func(self):
        # Verifica si el usuario pertenece al grupo 'comisariaprimera'.
        return user_is_in_group(self.request.user, 'comisariaprimera')

    # Método que maneja el caso en el que el usuario no tiene permiso para acceder a la vista.
    def handle_no_permission(self):
        # Redirige al usuario a la página de 'no_permission' si no tiene permiso.
        return redirect('no_permission')

    # Método que personaliza el conjunto de datos que se listará en la vista.
    def get_queryset(self):
        # Obtiene el queryset predeterminado y lo ordena por la fecha y hora en orden descendente.
        #queryset = super().get_queryset().order_by('-fecha_hora')
        queryset = super().get_queryset().filter(activo=True).order_by('-fecha_hora')
        # Obtiene el parámetro de búsqueda de la solicitud GET, si existe.
        search_query = self.request.GET.get('q', '')
        
        # Si hay una consulta de búsqueda, filtra el queryset por coincidencias en el campo 'cuarto'.
        if search_query:
            queryset = queryset.filter(cuarto__cuarto__icontains=search_query)
        
        # Ajusta la fecha y hora de cada registro en el queryset para asegurarse de que estén en la zona horaria local.
        for comisaria in queryset:
            if timezone.is_naive(comisaria.fecha_hora):
                # Si la fecha y hora son ingenuas (sin zona horaria), se convierten a la zona horaria actual.
                comisaria.fecha_hora = timezone.make_aware(comisaria.fecha_hora, timezone.get_current_timezone())
            
            # Convierte la fecha y hora a la hora local.
            comisaria.fecha_hora = timezone.localtime(comisaria.fecha_hora)
        
        # Devuelve el queryset final, posiblemente filtrado y ajustado.
        return queryset

    # Método que proporciona datos adicionales al contexto de la plantilla.
    def get_context_data(self, **kwargs):
        # Llama al método original para obtener el contexto predeterminado.
        context = super().get_context_data(**kwargs)

        user = self.request.user
        
        # Agrega al contexto un booleano que indica si el usuario pertenece al grupo 'jefessuperiores'.
       # context['is_jefessuperiores'] = self.request.user.groups.filter(name='jefessuperiores').exists()

          # Verificar la pertenencia a los grupos
          
        
        #context['is_encargados_guardias_primera'] = user.groups.filter(name='encargados_guardias_primera').exists()
        #context['is_jefessuperiores'] = user.groups.filter(name='jefessuperiores').exists()
        #context['is_oficialesservicios'] = user.groups.filter(name='oficialesservicios').exists()
        #context['is_comisariaprimera'] = user.groups.filter(name='comisariaprimera').exists()

        context['is_jefessuperiores'] = user.groups.filter(name='jefessuperiores').exists()
        context['is_libreros'] = user.groups.filter(name='libreros').exists()
        context['is_encargadosguardias'] = user.groups.filter(name='encargadosguardias').exists()
        context['is_oficialesservicios'] = user.groups.filter(name='oficialesservicios').exists()
        context['is_comisariaprimera'] = user.groups.filter(name='comisariaprimera').exists()
        
        # Agrega la fecha actual al contexto.
        context['today'] = timezone.now().date()
        
        # Inicializa resolveId en None y lo agrega al contexto.
        context['resolveId'] = None  # Inicializa resolveId en None
        
        # Devuelve el contexto completo.
        return context

#---------------------------clase para el create del formulario------------------------------------------------------------------------------------
   


class ComisariaPrimeraCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    # Especifica el modelo de datos que se va a crear.
    model = ComisariaPrimera
    
    # Especifica el formulario que se utilizará para crear el objeto.
    form_class = ComisariaPrimeraForm
    
    # Define la plantilla que se utilizará para renderizar el formulario.
    template_name = 'comisarias/primera/comisaria_primera_form.html'
    
    # Define la URL a la que se redirigirá al usuario después de crear el objeto.
    success_url = reverse_lazy('comisaria_primera_list')

    # Método que determina si el usuario tiene permiso para acceder a esta vista.
    def test_func(self):
        # Verifica si el usuario pertenece al grupo 'comisariaprimera'.
        return user_is_in_group(self.request.user, 'comisariaprimera')

    # Método que maneja el caso en el que el usuario no tiene permiso para acceder a la vista.
    def handle_no_permission(self):
        # Redirige al usuario a la página de 'no_permission' si no tiene

                # Redirige al usuario a la página de 'no_permission' si no tiene permiso.
        return redirect('no_permission')

    # Método que proporciona datos adicionales al contexto de la plantilla.
    def get_context_data(self, **kwargs):
        # Llama al método original para obtener el contexto predeterminado.
        context = super().get_context_data(**kwargs)
        
        # Añade al contexto todos los objetos de CodigoPolicialUSH.
        context['codigos_policiales'] = CodigoPolicialUSH.objects.all()
        
        # Añade al contexto todos los objetos de DependenciasSecundarias.
       # context['dependencias_secundarias'] = DependenciasSecundarias.objects.all()

        # Inicializa detalles adicionales como listas vacías en el contexto para la vista de creación.
        context['detalle_servicios_emergencia'] = json.dumps([])
        context['detalle_instituciones_hospitalarias'] = json.dumps([])
        context['detalle_dependencias_municipales'] = json.dumps([])
        context['detalle_dependencias_provinciales'] = json.dumps([])
        context['detalle_dependencias_secundarias'] = json.dumps([])
        context['detalle_instituciones_federales'] = json.dumps([])  # Añadido para federales

        # Devuelve el contexto completo para ser utilizado en la plantilla.
        return context

    # Método que se llama cuando el formulario es válido.
    def form_valid(self, form):
            # Guarda el objeto pero sin enviarlo aún a la base de datos.
            self.object = form.save(commit=False)
            
            # Asigna al campo 'created_by' el usuario actual.
            self.object.created_by = self.request.user
            
            # Inicializa los campos 'updated_by' y 'updated_at' como None.
            self.object.updated_by = None
            self.object.updated_at = None

            # Obtiene la latitud y longitud desde el formulario y convierte las comas en puntos.
            latitude = self.request.POST.get('latitude').replace(',', '.')
            longitude = self.request.POST.get('longitude').replace(',', '.')

            # Asigna las coordenadas al objeto si están disponibles.
            self.object.latitude = float(latitude) if latitude else None
            self.object.longitude = float(longitude) if longitude else None

            # Guarda el objeto en la base de datos.
            self.object.save()
            
            # Guarda las relaciones many-to-many del formulario.
            form.save_m2m()

            # Guardar los detalles adicionales para cada servicio de emergencia.
            for servicio in form.cleaned_data['servicios_emergencia']:
                # Obtiene los datos específicos para cada servicio de emergencia desde el formulario.
                numero_movil_bomberos = self.request.POST.get(f'numero_movil_bomberos_{servicio.id}')
                nombre_a_cargo_bomberos = self.request.POST.get(f'nombre_a_cargo_bomberos_{servicio.id}')
                
                # Si se proporcionan datos, crea un registro en DetalleServicioEmergencia.
                if numero_movil_bomberos or nombre_a_cargo_bomberos:
                    DetalleServicioEmergencia.objects.create(
                        servicio_emergencia=servicio,
                        comisaria_primera=self.object,
                        numero_movil_bomberos=numero_movil_bomberos,
                        nombre_a_cargo_bomberos=nombre_a_cargo_bomberos
                    )

            # Guardar los detalles adicionales para cada institución hospitalaria.
            for institucion in form.cleaned_data['instituciones_hospitalarias']:
                # Obtiene los datos específicos para cada institución hospitalaria desde el formulario.
                numero_movil_hospital = self.request.POST.get(f'numero_movil_hospital_{institucion.id}')
                nombre_a_cargo_hospital = self.request.POST.get(f'nombre_a_cargo_hospital_{institucion.id}')
                
                # Si se proporcionan datos, crea un registro en DetalleInstitucionHospitalaria.
                if numero_movil_hospital or nombre_a_cargo_hospital:
                    DetalleInstitucionHospitalaria.objects.create(
                        institucion_hospitalaria=institucion,
                        comisaria_primera=self.object,
                        numero_movil_hospital=numero_movil_hospital,
                        nombre_a_cargo_hospital=nombre_a_cargo_hospital
                    )

            # Guardar los detalles adicionales para cada dependencia municipal.
            for dependencia_municipal in form.cleaned_data['dependencias_municipales']:
                # Obtiene los datos específicos para cada dependencia municipal desde el formulario.
                numero_movil_municipal = self.request.POST.get(f'numero_movil_municipal_{dependencia_municipal.id}')
                nombre_a_cargo_municipal = self.request.POST.get(f'nombre_a_cargo_municipal_{dependencia_municipal.id}')
                
                # Si se proporcionan datos, crea un registro en DetalleDependenciaMunicipal.
                if numero_movil_municipal or nombre_a_cargo_municipal:
                    DetalleDependenciaMunicipal.objects.create(
                        dependencia_municipal=dependencia_municipal,
                        comisaria_primera=self.object,
                        numero_movil_municipal=numero_movil_municipal,
                        nombre_a_cargo_municipal=nombre_a_cargo_municipal
                    )

            # Guardar los detalles adicionales para cada dependencia provincial.
            for dependencia_provincial in form.cleaned_data['dependencias_provinciales']:
                # Obtiene los datos específicos para cada dependencia provincial desde el formulario.
                numero_movil_provincial = self.request.POST.get(f'numero_movil_provincial_{dependencia_provincial.id}')
                nombre_a_cargo_provincial = self.request.POST.get(f'nombre_a_cargo_provincial_{dependencia_provincial.id}')
                
                # Si se proporcionan datos, crea un registro en DetalleDependenciaProvincial.
                if numero_movil_provincial or nombre_a_cargo_provincial:
                    DetalleDependenciaProvincial.objects.create(
                        dependencia_provincial=dependencia_provincial,
                        comisaria_primera=self.object,
                        numero_movil_provincial=numero_movil_provincial,
                        nombre_a_cargo_provincial=nombre_a_cargo_provincial
                    )

            # Guardar los detalles adicionales para dependencias secundarias
            for dependencia_secundaria in form.cleaned_data['dependencias_secundarias']:
                numero_movil_secundaria = self.request.POST.get(f'numero_movil_secundaria_{dependencia_secundaria.id}')
                nombre_a_cargo_secundaria = self.request.POST.get(f'nombre_a_cargo_secundaria_{dependencia_secundaria.id}')
                if numero_movil_secundaria or nombre_a_cargo_secundaria:
                    DetalleDependenciaSecundaria.objects.create(
                        dependencia_secundaria=dependencia_secundaria,
                        comisaria_primera=self.object,
                        numero_movil_secundaria=numero_movil_secundaria,
                        nombre_a_cargo_secundaria=nombre_a_cargo_secundaria
                    )

            # Guardar los detalles adicionales para instituciones federales
            for institucion_federal in form.cleaned_data['instituciones_federales']:
                numero_movil_federal = self.request.POST.get(f'numero_movil_federal_{institucion_federal.id}')
                nombre_a_cargo_federal = self.request.POST.get(f'nombre_a_cargo_federal_{institucion_federal.id}')
                if numero_movil_federal or nombre_a_cargo_federal:
                    DetalleInstitucionFederal.objects.create(
                        institucion_federal=institucion_federal,
                        comisaria_primera=self.object,
                        numero_movil_federal=numero_movil_federal,
                        nombre_a_cargo_federal=nombre_a_cargo_federal
                    )        

            # Llama al método form_valid de la clase base para completar la operación.
            # Añadir un mensaje de éxito al sistema de mensajes
            messages.success(self.request, 'El código ha sido guardado exitosamente.')
            
            return super().form_valid(form)
       

 #------------------------clase para el edit updtae------------------------------------------------------


class ComisariaPrimeraUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # Especifica el modelo de datos que se va a actualizar.
    model = ComisariaPrimera
    
    # Especifica el formulario que se utilizará para actualizar el objeto.
    form_class = ComisariaPrimeraForm
    
    # Define la plantilla que se utilizará para renderizar el formulario.
    template_name = 'comisarias/primera/comisaria_primera_form.html'
    
    # Define la URL a la que se redirigirá al usuario después de actualizar el objeto.
    success_url = reverse_lazy('comisaria_primera_list')

    # Método que determina si el usuario tiene permiso para acceder a esta vista.
    def test_func(self):
        # Verifica si el usuario pertenece al grupo 'comisariaprimera'.
        return user_is_in_group(self.request.user, 'comisariaprimera')

    # Método que maneja el caso en el que el usuario no tiene permiso para acceder a la vista.
    def handle_no_permission(self):
        # Redirige al usuario a la página de 'no_permission' si no tiene permiso.
        return redirect('no_permission')

    # Método para personalizar el proceso de despacho de la solicitud.
    def dispatch(self, request, *args, **kwargs):
        # Obtiene el objeto que se va a actualizar.
        obj = self.get_object()
        
        # Obtiene la fecha y hora actuales.
        now = timezone.now()

        # Verifica si la fecha del objeto no es hoy y si el estado no está activo.
        if obj.fecha_hora.date() != now.date() and not obj.estado:
            # Si es así, redirige a la lista de comisarias.
            return redirect('comisaria_primera_list')

        # Si no se cumplen las condiciones anteriores, sigue con el proceso normal.
        return super().dispatch(request, *args, **kwargs)

    # Método que proporciona datos adicionales al contexto de la plantilla.
    def get_context_data(self, **kwargs):
        # Llama al método original para obtener el contexto predeterminado.
        context = super().get_context_data(**kwargs)
        
        # Añade al contexto todos los objetos de CodigoPolicialUSH.
        context['codigos_policiales'] = CodigoPolicialUSH.objects.all()
        
        # Añade al contexto todos los objetos de DependenciasSecundarias.
       # context['dependencias_secundarias'] = DependenciasSecundarias.objects.all()

        # Convierte los detalles en JSON para ser usados por Alpine.js
        context['detalle_servicios_emergencia'] = json.dumps(list(
            DetalleServicioEmergencia.objects.filter(comisaria_primera=self.object.pk).values('id', 'servicio_emergencia_id', 'numero_movil_bomberos', 'nombre_a_cargo_bomberos')
        ))

        context['detalle_instituciones_hospitalarias'] = json.dumps(list(
            DetalleInstitucionHospitalaria.objects.filter(comisaria_primera=self.object.pk).values('id', 'institucion_hospitalaria_id', 'numero_movil_hospital', 'nombre_a_cargo_hospital')
        ))

        context['detalle_dependencias_municipales'] = json.dumps(list(
            DetalleDependenciaMunicipal.objects.filter(comisaria_primera=self.object.pk).values('id', 'dependencia_municipal_id', 'numero_movil_municipal', 'nombre_a_cargo_municipal')
        ))

        context['detalle_dependencias_provinciales'] = json.dumps(list(
            DetalleDependenciaProvincial.objects.filter(comisaria_primera=self.object.pk).values('id', 'dependencia_provincial_id', 'numero_movil_provincial', 'nombre_a_cargo_provincial')
        ))

         # Añadir los nuevos detalles para dependencias secundarias
        context['detalle_dependencias_secundarias'] = json.dumps(list(
            DetalleDependenciaSecundaria.objects.filter(comisaria_primera=self.object.pk).values('id', 'dependencia_secundaria_id', 'numero_movil_secundaria', 'nombre_a_cargo_secundaria')
        ))

        # Añadir los nuevos detalles para instituciones federales
        context['detalle_instituciones_federales'] = json.dumps(list(
            DetalleInstitucionFederal.objects.filter(comisaria_primera=self.object.pk).values('id', 'institucion_federal_id', 'numero_movil_federal', 'nombre_a_cargo_federal')
        ))

        # Devuelve el contexto completo para ser utilizado en la plantilla.
        return context

    # Método que se llama cuando el formulario es válido.
    def form_valid(self, form):
        # Guarda el objeto pero sin enviarlo aún a la base de datos.
        self.object = form.save(commit=False)
        
        # Asigna al campo 'updated_by' el usuario actual.
        self.object.updated_by = self.request.user
        
        # Asigna al campo 'updated_at' la fecha y hora actuales.
        self.object.updated_at = timezone.now()

        # Obtiene la latitud y longitud desde el formulario y convierte las comas en puntos.
        latitude = self.request.POST.get('latitude').replace(',', '.')
        longitude = self.request.POST.get('longitude').replace(',', '.')

        # Asigna las coordenadas al objeto si están disponibles.
        self.object.latitude = float(latitude) if latitude else None
        self.object.longitude = float(longitude) if longitude else None

        # Guarda el objeto en la base de datos.
        self.object.save()
        
        # Guarda las relaciones many-to-many del formulario.
        form.save_m2m()

        # Mantener un registro de los IDs seleccionados.
        servicios_emergencia_ids = form.cleaned_data['servicios_emergencia'].values_list('id', flat=True)
        instituciones_hospitalarias_ids = form.cleaned_data['instituciones_hospitalarias'].values_list('id', flat=True)
        dependencias_municipales_ids = form.cleaned_data['dependencias_municipales'].values_list('id', flat=True)
        dependencias_provinciales_ids = form.cleaned_data['dependencias_provinciales'].values_list('id', flat=True)
        dependencias_secundarias_ids = form.cleaned_data['dependencias_secundarias'].values_list('id', flat=True)
        instituciones_federales_ids = form.cleaned_data['instituciones_federales'].values_list('id', flat=True)


        # Eliminar los detalles que ya no están seleccionados.
        DetalleServicioEmergencia.objects.filter(comisaria_primera=self.object).exclude(servicio_emergencia_id__in=servicios_emergencia_ids).delete()
        DetalleInstitucionHospitalaria.objects.filter(comisaria_primera=self.object).exclude(institucion_hospitalaria_id__in=instituciones_hospitalarias_ids).delete()
        DetalleDependenciaMunicipal.objects.filter(comisaria_primera=self.object).exclude(dependencia_municipal_id__in=dependencias_municipales_ids).delete()
        DetalleDependenciaProvincial.objects.filter(comisaria_primera=self.object).exclude(dependencia_provincial_id__in=dependencias_provinciales_ids).delete()
        DetalleDependenciaSecundaria.objects.filter(comisaria_primera=self.object).exclude(dependencia_secundaria_id__in=dependencias_secundarias_ids).delete()
        DetalleInstitucionFederal.objects.filter(comisaria_primera=self.object).exclude(institucion_federal_id__in=instituciones_federales_ids).delete()


        # Guardar los detalles adicionales para cada servicio de emergencia.
        for servicio in form.cleaned_data['servicios_emergencia']:
            numero_movil_bomberos = self.request.POST.get(f'numero_movil_bomberos_{servicio.id}')
            nombre_a_cargo_bomberos = self.request.POST.get(f'nombre_a_cargo_bomberos_{servicio.id}')
            DetalleServicioEmergencia.objects.update_or_create(
                servicio_emergencia=servicio,
                comisaria_primera=self.object,
                defaults={
                    'numero_movil_bomberos': numero_movil_bomberos,
                    'nombre_a_cargo_bomberos': nombre_a_cargo_bomberos
                }
            )

        # Guardar los detalles adicionales para cada institución hospitalaria.
        for institucion in form.cleaned_data['instituciones_hospitalarias']:
            numero_movil_hospital = self.request.POST.get(f'numero_movil_hospital_{institucion.id}')
            nombre_a_cargo_hospital = self.request.POST.get(f'nombre_a_cargo_hospital_{institucion.id}')
            DetalleInstitucionHospitalaria.objects.update_or_create(
                institucion_hospitalaria=institucion,
                comisaria_primera=self.object,
                defaults={
                    'numero_movil_hospital': numero_movil_hospital,
                    'nombre_a_cargo_hospital': nombre_a_cargo_hospital
                }
            )

        # Guardar los detalles adicionales para cada dependencia municipal.
        for dependencia_municipal in form.cleaned_data['dependencias_municipales']:
            numero_movil_municipal = self.request.POST.get(f'numero_movil_municipal_{dependencia_municipal.id}')
            nombre_a_cargo_municipal = self.request.POST.get(f'nombre_a_cargo_municipal_{dependencia_municipal.id}')
            DetalleDependenciaMunicipal.objects.update_or_create(
                dependencia_municipal=dependencia_municipal,
                comisaria_primera=self.object,
                defaults={
                    'numero_movil_municipal': numero_movil_municipal,
                    'nombre_a_cargo_municipal': nombre_a_cargo_municipal
                }
            )

        # Guardar los detalles adicionales para cada dependencia provincial.
        for dependencia_provincial in form.cleaned_data['dependencias_provinciales']:
            numero_movil_provincial = self.request.POST.get(f'numero_movil_provincial_{dependencia_provincial.id}')
            nombre_a_cargo_provincial = self.request.POST.get(f'nombre_a_cargo_provincial_{dependencia_provincial.id}')
            DetalleDependenciaProvincial.objects.update_or_create(
                dependencia_provincial=dependencia_provincial,
                comisaria_primera=self.object,
                defaults={
                    'numero_movil_provincial': numero_movil_provincial,
                    'nombre_a_cargo_provincial': nombre_a_cargo_provincial
                }
            )

          # Guardar detalles adicionales para cada dependencia secundaria
        for dependencia_secundaria in form.cleaned_data['dependencias_secundarias']:
            numero_movil_secundaria = self.request.POST.get(f'numero_movil_secundaria_{dependencia_secundaria.id}')
            nombre_a_cargo_secundaria = self.request.POST.get(f'nombre_a_cargo_secundaria_{dependencia_secundaria.id}')
            DetalleDependenciaSecundaria.objects.update_or_create(
                dependencia_secundaria=dependencia_secundaria,
                comisaria_primera=self.object,
                defaults={
                    'numero_movil_secundaria': numero_movil_secundaria,
                    'nombre_a_cargo_secundaria': nombre_a_cargo_secundaria
                }
            )

        # Guardar detalles adicionales para instituciones federales
        for institucion_federal in form.cleaned_data['instituciones_federales']:
            numero_movil_federal = self.request.POST.get(f'numero_movil_federal_{institucion_federal.id}')
            nombre_a_cargo_federal = self.request.POST.get(f'nombre_a_cargo_federal_{institucion_federal.id}')
            DetalleInstitucionFederal.objects.update_or_create(
                institucion_federal=institucion_federal,
                comisaria_primera=self.object,
                defaults={
                    'numero_movil_federal': numero_movil_federal,
                    'nombre_a_cargo_federal': nombre_a_cargo_federal
                }
            )    

             # Añadir el mensaje de éxito
       # messages.success(self.request, 'El código ha sido editado exitosamente.')
        messages.success(self.request, 'El código ha sido guardado exitosamente.')

        # Llama al método form_valid de la clase base para completar la operación.
        return super().form_valid(form)

#--------------------------viesta para ver todos completo cada regitro--------------------------------------------------



class ComisariaPrimeraDetailView(DetailView):
    model = ComisariaPrimera
    template_name = 'comisarias/primera/comisaria_primera_detail.html'
    context_object_name = 'record'




#----------------------------softdelete-------------------------------------------------------------

# En views.py

def eliminar_comisaria_primera(request, pk):
    # Obtén el registro a eliminar
    comisaria = get_object_or_404(ComisariaPrimera, pk=pk)
    
    # Marca el registro como inactivo
    comisaria.activo = False
    comisaria.save()
    
    # Envía un mensaje de confirmación
    messages.success(request, 'El código ha sido eliminado correctamente.')
    
    # Redirige de vuelta a la lista
    return redirect('comisaria_primera_list')




#---------------------------------------------------------------------------------------------------------------------------------------


# Vistas de listado y creación para ComisariaSegunda, ComisariaTercera, ComisariaCuarta, y ComisariaQuinta


class ComisariaSegundaListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ComisariaSegunda
    template_name = 'comisarias/segunda/comisaria_segunda_list.html'
    context_object_name = 'records'

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariasegunda')

    def handle_no_permission(self):
        return redirect('no_permission')
    

    def get_queryset(self):
        #queryset = super().get_queryset().order_by('-fecha_hora')
        queryset = super().get_queryset().filter(activo=True).order_by('-fecha_hora')
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(cuarto__cuarto__icontains=search_query)
        for comisaria in queryset:
            if timezone.is_naive(comisaria.fecha_hora):
                comisaria.fecha_hora = timezone.make_aware(comisaria.fecha_hora, timezone.get_current_timezone())
            comisaria.fecha_hora = timezone.localtime(comisaria.fecha_hora)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        #context['is_jefessuperiores'] = self.request.user.groups.filter(name='jefessuperiores').exists()
        #context['is_encargados_guardias_segunda'] = user.groups.filter(name='encargados_guardias_segunda').exists()
        context['is_jefessuperiores'] = user.groups.filter(name='jefessuperiores').exists()
        context['is_libreros'] = user.groups.filter(name='libreros').exists()
        context['is_encargadosguardias'] = user.groups.filter(name='encargadosguardias').exists()
        context['is_oficialesservicios'] = user.groups.filter(name='oficialesservicios').exists()
        context['is_comisariasegunda'] = user.groups.filter(name='comisariasegunda').exists()


        context['today'] = timezone.now().date()
        context['resolveId'] = None
        return context

#-----------------------------------------------------------------------------------------------------------------   
    

class ComisariaSegundaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ComisariaSegunda
    form_class = ComisariaSegundaForm
    template_name = 'comisarias/segunda/comisaria_segunda_form.html'
    success_url = reverse_lazy('comisaria_segunda_list')

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariasegunda')

    def handle_no_permission(self):
        return redirect('no_permission')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['codigos_policiales'] = CodigoPolicialUSH.objects.all()
        #context['dependencias_secundarias'] = DependenciasSecundarias.objects.all()

        # Inicializar detalles como listas vacías en el contexto
        context['detalle_servicios_emergencia'] = json.dumps([])  # Para vista de creación, siempre es una lista vacía
        context['detalle_instituciones_hospitalarias'] = json.dumps([])
        context['detalle_dependencias_municipales'] = json.dumps([])
        context['detalle_dependencias_provinciales'] = json.dumps([])
        context['detalle_dependencias_secundarias'] = json.dumps([])
        context['detalle_instituciones_federales'] = json.dumps([])  # Añadido para federales



        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.updated_by = None
        self.object.updated_at = None

        latitude = self.request.POST.get('latitude').replace(',', '.')
        longitude = self.request.POST.get('longitude').replace(',', '.')

        self.object.latitude = float(latitude) if latitude else None
        self.object.longitude = float(longitude) if longitude else None

        self.object.save()
        form.save_m2m()

        # Guardar los detalles adicionales para cada servicio de emergencia
        for servicio in form.cleaned_data['servicios_emergencia']:
            numero_movil_bomberos = self.request.POST.get(f'numero_movil_bomberos_{servicio.id}')
            nombre_a_cargo_bomberos = self.request.POST.get(f'nombre_a_cargo_bomberos_{servicio.id}')
            if numero_movil_bomberos or nombre_a_cargo_bomberos:
                DetalleServicioEmergencia.objects.create(
                    servicio_emergencia=servicio,
                    comisaria_segunda=self.object,
                    numero_movil_bomberos=numero_movil_bomberos,
                    nombre_a_cargo_bomberos=nombre_a_cargo_bomberos
                )

        # Guardar los detalles adicionales para cada institución hospitalaria
        for institucion in form.cleaned_data['instituciones_hospitalarias']:
            numero_movil_hospital = self.request.POST.get(f'numero_movil_hospital_{institucion.id}')
            nombre_a_cargo_hospital = self.request.POST.get(f'nombre_a_cargo_hospital_{institucion.id}')
            if numero_movil_hospital or nombre_a_cargo_hospital:
                DetalleInstitucionHospitalaria.objects.create(
                    institucion_hospitalaria=institucion,
                    comisaria_segunda=self.object,
                    numero_movil_hospital=numero_movil_hospital,
                    nombre_a_cargo_hospital=nombre_a_cargo_hospital
                )

        # Guardar los detalles adicionales para cada dependencia municipal
        for dependencia_municipal in form.cleaned_data['dependencias_municipales']:
            numero_movil_municipal = self.request.POST.get(f'numero_movil_municipal_{dependencia_municipal.id}')
            nombre_a_cargo_municipal = self.request.POST.get(f'nombre_a_cargo_municipal_{dependencia_municipal.id}')
            if numero_movil_municipal or nombre_a_cargo_municipal:
                DetalleDependenciaMunicipal.objects.create(
                    dependencia_municipal=dependencia_municipal,
                    comisaria_segunda=self.object,
                    numero_movil_municipal=numero_movil_municipal,
                    nombre_a_cargo_municipal=nombre_a_cargo_municipal
                )

        # Guardar los detalles adicionales para cada dependencia provincial
        for dependencia_provincial in form.cleaned_data['dependencias_provinciales']:
            numero_movil_provincial = self.request.POST.get(f'numero_movil_provincial_{dependencia_provincial.id}')
            nombre_a_cargo_provincial = self.request.POST.get(f'nombre_a_cargo_provincial_{dependencia_provincial.id}')
            if numero_movil_provincial or nombre_a_cargo_provincial:
                DetalleDependenciaProvincial.objects.create(
                    dependencia_provincial=dependencia_provincial,
                    comisaria_segunda=self.object,
                    numero_movil_provincial=numero_movil_provincial,
                    nombre_a_cargo_provincial=nombre_a_cargo_provincial
                )

         # Guardar los detalles adicionales para dependencias secundarias
        for dependencia_secundaria in form.cleaned_data['dependencias_secundarias']:
            numero_movil_secundaria = self.request.POST.get(f'numero_movil_secundaria_{dependencia_secundaria.id}')
            nombre_a_cargo_secundaria = self.request.POST.get(f'nombre_a_cargo_secundaria_{dependencia_secundaria.id}')
            if numero_movil_secundaria or nombre_a_cargo_secundaria:
                DetalleDependenciaSecundaria.objects.create(
                    dependencia_secundaria=dependencia_secundaria,
                    comisaria_segunda=self.object,
                    numero_movil_secundaria=numero_movil_secundaria,
                    nombre_a_cargo_secundaria=nombre_a_cargo_secundaria
                )

        # Guardar los detalles adicionales para instituciones federales
        for institucion_federal in form.cleaned_data['instituciones_federales']:
            numero_movil_federal = self.request.POST.get(f'numero_movil_federal_{institucion_federal.id}')
            nombre_a_cargo_federal = self.request.POST.get(f'nombre_a_cargo_federal_{institucion_federal.id}')
            if numero_movil_federal or nombre_a_cargo_federal:
                DetalleInstitucionFederal.objects.create(
                    institucion_federal=institucion_federal,
                    comisaria_segunda=self.object,
                    numero_movil_federal=numero_movil_federal,
                    nombre_a_cargo_federal=nombre_a_cargo_federal
                )         


        messages.success(self.request, 'El código ha sido guardado exitosamente.')
        return super().form_valid(form)


#--------------------------------------------------------------------------------------------------

class ComisariaSegundaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ComisariaSegunda
    form_class = ComisariaSegundaForm
    template_name = 'comisarias/segunda/comisaria_segunda_form.html'
    success_url = reverse_lazy('comisaria_segunda_list')

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariasegunda')

    def handle_no_permission(self):
        return redirect('no_permission')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        now = timezone.now()

        if obj.fecha_hora.date() != now.date() and not obj.estado:
            return redirect('comisaria_segunda_list')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['codigos_policiales'] = CodigoPolicialUSH.objects.all()
        #context['dependencias_secundarias'] = DependenciasSecundarias.objects.all()

        # Convertir detalles en JSON para ser usados por Alpine.js
        context['detalle_servicios_emergencia'] = json.dumps(list(
            DetalleServicioEmergencia.objects.filter(comisaria_segunda=self.object.pk).values('id', 'servicio_emergencia_id', 'numero_movil_bomberos', 'nombre_a_cargo_bomberos')
        ))

        context['detalle_instituciones_hospitalarias'] = json.dumps(list(
            DetalleInstitucionHospitalaria.objects.filter(comisaria_segunda=self.object.pk).values('id', 'institucion_hospitalaria_id', 'numero_movil_hospital', 'nombre_a_cargo_hospital')
        ))

        context['detalle_dependencias_municipales'] = json.dumps(list(
            DetalleDependenciaMunicipal.objects.filter(comisaria_segunda=self.object.pk).values('id', 'dependencia_municipal_id', 'numero_movil_municipal', 'nombre_a_cargo_municipal')
        ))

        context['detalle_dependencias_provinciales'] = json.dumps(list(
            DetalleDependenciaProvincial.objects.filter(comisaria_segunda=self.object.pk).values('id', 'dependencia_provincial_id', 'numero_movil_provincial', 'nombre_a_cargo_provincial')
        ))

        # Añadir los nuevos detalles para dependencias secundarias
        context['detalle_dependencias_secundarias'] = json.dumps(list(
            DetalleDependenciaSecundaria.objects.filter(comisaria_segunda=self.object.pk).values('id', 'dependencia_secundaria_id', 'numero_movil_secundaria', 'nombre_a_cargo_secundaria')
        ))

        # Añadir los nuevos detalles para instituciones federales
        context['detalle_instituciones_federales'] = json.dumps(list(
            DetalleInstitucionFederal.objects.filter(comisaria_segunda=self.object.pk).values('id', 'institucion_federal_id', 'numero_movil_federal', 'nombre_a_cargo_federal')
        ))

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_by = self.request.user
        self.object.updated_at = timezone.now()

        latitude = self.request.POST.get('latitude').replace(',', '.')
        longitude = self.request.POST.get('longitude').replace(',', '.')

        self.object.latitude = float(latitude) if latitude else None
        self.object.longitude = float(longitude) if longitude else None

        self.object.save()
        form.save_m2m()

        # Mantener un registro de los IDs seleccionados
        servicios_emergencia_ids = form.cleaned_data['servicios_emergencia'].values_list('id', flat=True)
        instituciones_hospitalarias_ids = form.cleaned_data['instituciones_hospitalarias'].values_list('id', flat=True)
        dependencias_municipales_ids = form.cleaned_data['dependencias_municipales'].values_list('id', flat=True)
        dependencias_provinciales_ids = form.cleaned_data['dependencias_provinciales'].values_list('id', flat=True)
        dependencias_secundarias_ids = form.cleaned_data['dependencias_secundarias'].values_list('id', flat=True)
        instituciones_federales_ids = form.cleaned_data['instituciones_federales'].values_list('id', flat=True)



        # Eliminar los detalles que ya no se arreglo están seleccionados
        DetalleServicioEmergencia.objects.filter(comisaria_segunda=self.object).exclude(servicio_emergencia_id__in=servicios_emergencia_ids).delete()
        DetalleInstitucionHospitalaria.objects.filter(comisaria_segunda=self.object).exclude(institucion_hospitalaria_id__in=instituciones_hospitalarias_ids).delete()
        DetalleDependenciaMunicipal.objects.filter(comisaria_segunda=self.object).exclude(dependencia_municipal_id__in=dependencias_municipales_ids).delete()
        DetalleDependenciaProvincial.objects.filter(comisaria_segunda=self.object).exclude(dependencia_provincial_id__in=dependencias_provinciales_ids).delete()
        DetalleDependenciaSecundaria.objects.filter(comisaria_segunda=self.object).exclude(dependencia_secundaria_id__in=dependencias_secundarias_ids).delete()
        DetalleInstitucionFederal.objects.filter(comisaria_segunda=self.object).exclude(institucion_federal_id__in=instituciones_federales_ids).delete()


        # Guardar los detalles adicionales para cada servicio de emergencia.
        for servicio in form.cleaned_data['servicios_emergencia']:
            # Obtiene el número de móvil del formulario correspondiente a cada servicio de emergencia.
            numero_movil_bomberos = self.request.POST.get(f'numero_movil_bomberos_{servicio.id}')
    
            # Obtiene el nombre de la persona a cargo del formulario correspondiente a cada servicio de emergencia.
            nombre_a_cargo_bomberos = self.request.POST.get(f'nombre_a_cargo_bomberos_{servicio.id}')
    
            # Crea o actualiza un registro en la tabla DetalleServicioEmergencia.
            DetalleServicioEmergencia.objects.update_or_create(

                 # Relaciona el registro con el servicio de emergencia actual.
                 servicio_emergencia=servicio,
        
                 # Relaciona el registro con la instancia de ComisariaSegunda que se está editando o creando.
                 comisaria_segunda=self.object,
        
                 # Define los valores predeterminados para los campos que se van a actualizar o crear.
                 defaults={
                    'numero_movil_bomberos': numero_movil_bomberos,  # Asigna el número de móvil obtenido del formulario.
                    'nombre_a_cargo_bomberos': nombre_a_cargo_bomberos  # Asigna el nombre de la persona a cargo obtenido del formulario.
                }
            )
    

        # Guardar los detalles adicionales para cada institución hospitalaria
        for institucion in form.cleaned_data['instituciones_hospitalarias']:
            numero_movil_hospital = self.request.POST.get(f'numero_movil_hospital_{institucion.id}')
            nombre_a_cargo_hospital = self.request.POST.get(f'nombre_a_cargo_hospital_{institucion.id}')
            DetalleInstitucionHospitalaria.objects.update_or_create(
                institucion_hospitalaria=institucion,
                comisaria_segunda=self.object,
                defaults={
                    'numero_movil_hospital': numero_movil_hospital,
                    'nombre_a_cargo_hospital': nombre_a_cargo_hospital
                }
            )

        # Guardar los detalles adicionales para cada dependencia municipal
        for dependencia_municipal in form.cleaned_data['dependencias_municipales']:
            numero_movil_municipal = self.request.POST.get(f'numero_movil_municipal_{dependencia_municipal.id}')
            nombre_a_cargo_municipal = self.request.POST.get(f'nombre_a_cargo_municipal_{dependencia_municipal.id}')
            DetalleDependenciaMunicipal.objects.update_or_create(
                dependencia_municipal=dependencia_municipal,
                comisaria_segunda=self.object,
                defaults={
                    'numero_movil_municipal': numero_movil_municipal,
                    'nombre_a_cargo_municipal': nombre_a_cargo_municipal
                }
            )

        # Guardar los detalles adicionales para cada dependencia provincial
        for dependencia_provincial in form.cleaned_data['dependencias_provinciales']:
            numero_movil_provincial = self.request.POST.get(f'numero_movil_provincial_{dependencia_provincial.id}')
            nombre_a_cargo_provincial = self.request.POST.get(f'nombre_a_cargo_provincial_{dependencia_provincial.id}')
            DetalleDependenciaProvincial.objects.update_or_create(
                dependencia_provincial=dependencia_provincial,
                comisaria_segunda=self.object,
                defaults={
                    'numero_movil_provincial': numero_movil_provincial,
                    'nombre_a_cargo_provincial': nombre_a_cargo_provincial
                }
            )

          # Guardar detalles adicionales para cada dependencia secundaria
        for dependencia_secundaria in form.cleaned_data['dependencias_secundarias']:
            numero_movil_secundaria = self.request.POST.get(f'numero_movil_secundaria_{dependencia_secundaria.id}')
            nombre_a_cargo_secundaria = self.request.POST.get(f'nombre_a_cargo_secundaria_{dependencia_secundaria.id}')
            DetalleDependenciaSecundaria.objects.update_or_create(
                dependencia_secundaria=dependencia_secundaria,
                comisaria_segunda=self.object,
                defaults={
                    'numero_movil_secundaria': numero_movil_secundaria,
                    'nombre_a_cargo_secundaria': nombre_a_cargo_secundaria
                }
            )

        # Guardar detalles adicionales para instituciones federales
        for institucion_federal in form.cleaned_data['instituciones_federales']:
            numero_movil_federal = self.request.POST.get(f'numero_movil_federal_{institucion_federal.id}')
            nombre_a_cargo_federal = self.request.POST.get(f'nombre_a_cargo_federal_{institucion_federal.id}')
            DetalleInstitucionFederal.objects.update_or_create(
                institucion_federal=institucion_federal,
                comisaria_segunda=self.object,
                defaults={
                    'numero_movil_federal': numero_movil_federal,
                    'nombre_a_cargo_federal': nombre_a_cargo_federal
                }
            )    

        messages.success(self.request, 'El código ha sido guardado exitosamente.')
        return super().form_valid(form)
    

#--------------------------vista para ver todos completo cada registro------------------------------------------------------


class ComisariaSegundaDetailView(DetailView):
    model = ComisariaSegunda
    template_name = 'comisarias/segunda/comisaria_segunda_detail.html'
    context_object_name = 'record'


#----------------------------softdelete-------------------------------------------------------------

# En views.py

def eliminar_comisaria_segunda(request, pk):
    # Obtén el registro a eliminar
    comisaria = get_object_or_404(ComisariaSegunda, pk=pk)
    
    # Marca el registro como inactivo
    comisaria.activo = False
    comisaria.save()
    
    # Envía un mensaje de confirmación
    messages.success(request, 'El código ha sido eliminado correctamente.')
    
    # Redirige de vuelta a la lista
    return redirect('comisaria_segunda_list')



#-------------------------VISTA DE COMISARIA TERCERA ---------------------------------------------------------------------------------------------------------


class ComisariaTerceraListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ComisariaTercera
    template_name = 'comisarias/tercera/comisaria_tercera_list.html'
    context_object_name = 'records'

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariatercera')

    def handle_no_permission(self):
        return redirect('no_permission')

    def get_queryset(self):
        #queryset = super().get_queryset().order_by('-fecha_hora')
        queryset = super().get_queryset().filter(activo=True).order_by('-fecha_hora')
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(cuarto__cuarto__icontains=search_query)
        for comisaria in queryset:
            if timezone.is_naive(comisaria.fecha_hora):
                comisaria.fecha_hora = timezone.make_aware(comisaria.fecha_hora, timezone.get_current_timezone())
            comisaria.fecha_hora = timezone.localtime(comisaria.fecha_hora)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['is_jefessuperiores'] = user.groups.filter(name='jefessuperiores').exists()
        context['is_libreros'] = user.groups.filter(name='libreros').exists()
        context['is_encargadosguardias'] = user.groups.filter(name='encargadosguardias').exists()
        context['is_oficialesservicios'] = user.groups.filter(name='oficialesservicios').exists()
        context['is_comisariatercera'] = user.groups.filter(name='comisariatercera').exists()

        context['today'] = timezone.now().date()
        context['resolveId'] = None
        return context


#----------------------------CREACION DE COMISARIA TERCERA----------------------------------------


class ComisariaTerceraCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ComisariaTercera
    form_class = ComisariaTerceraForm
    template_name = 'comisarias/tercera/comisaria_tercera_form.html'
    success_url = reverse_lazy('comisaria_tercera_list')

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariatercera')

    def handle_no_permission(self):
        return redirect('no_permission')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['codigos_policiales'] = CodigoPolicialUSH.objects.all()

        # Inicializar detalles como listas vacías en el contexto
        context['detalle_servicios_emergencia'] = json.dumps([])  # Para vista de creación, siempre es una lista vacía
        context['detalle_instituciones_hospitalarias'] = json.dumps([])
        context['detalle_dependencias_municipales'] = json.dumps([])
        context['detalle_dependencias_provinciales'] = json.dumps([])
        context['detalle_dependencias_secundarias'] = json.dumps([])
        context['detalle_instituciones_federales'] = json.dumps([])  # Añadido para federales

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.updated_by = None
        self.object.updated_at = None

        latitude = self.request.POST.get('latitude').replace(',', '.')
        longitude = self.request.POST.get('longitude').replace(',', '.')

        self.object.latitude = float(latitude) if latitude else None
        self.object.longitude = float(longitude) if longitude else None

        self.object.save()
        form.save_m2m()

        # Guardar los detalles adicionales para cada servicio de emergencia
        for servicio in form.cleaned_data['servicios_emergencia']:
            numero_movil_bomberos = self.request.POST.get(f'numero_movil_bomberos_{servicio.id}')
            nombre_a_cargo_bomberos = self.request.POST.get(f'nombre_a_cargo_bomberos_{servicio.id}')
            if numero_movil_bomberos or nombre_a_cargo_bomberos:
                DetalleServicioEmergencia.objects.create(
                    servicio_emergencia=servicio,
                    comisaria_tercera=self.object,
                    numero_movil_bomberos=numero_movil_bomberos,
                    nombre_a_cargo_bomberos=nombre_a_cargo_bomberos
                )

        # Guardar los detalles adicionales para cada institución hospitalaria
        for institucion in form.cleaned_data['instituciones_hospitalarias']:
            numero_movil_hospital = self.request.POST.get(f'numero_movil_hospital_{institucion.id}')
            nombre_a_cargo_hospital = self.request.POST.get(f'nombre_a_cargo_hospital_{institucion.id}')
            if numero_movil_hospital or nombre_a_cargo_hospital:
                DetalleInstitucionHospitalaria.objects.create(
                    institucion_hospitalaria=institucion,
                    comisaria_tercera=self.object,
                    numero_movil_hospital=numero_movil_hospital,
                    nombre_a_cargo_hospital=nombre_a_cargo_hospital
                )

        # Guardar los detalles adicionales para cada dependencia municipal
        for dependencia_municipal in form.cleaned_data['dependencias_municipales']:
            numero_movil_municipal = self.request.POST.get(f'numero_movil_municipal_{dependencia_municipal.id}')
            nombre_a_cargo_municipal = self.request.POST.get(f'nombre_a_cargo_municipal_{dependencia_municipal.id}')
            if numero_movil_municipal or nombre_a_cargo_municipal:
                DetalleDependenciaMunicipal.objects.create(
                    dependencia_municipal=dependencia_municipal,
                    comisaria_tercera=self.object,
                    numero_movil_municipal=numero_movil_municipal,
                    nombre_a_cargo_municipal=nombre_a_cargo_municipal
                )

        # Guardar los detalles adicionales para cada dependencia provincial
        for dependencia_provincial in form.cleaned_data['dependencias_provinciales']:
            numero_movil_provincial = self.request.POST.get(f'numero_movil_provincial_{dependencia_provincial.id}')
            nombre_a_cargo_provincial = self.request.POST.get(f'nombre_a_cargo_provincial_{dependencia_provincial.id}')
            if numero_movil_provincial or nombre_a_cargo_provincial:
                DetalleDependenciaProvincial.objects.create(
                    dependencia_provincial=dependencia_provincial,
                    comisaria_tercera=self.object,
                    numero_movil_provincial=numero_movil_provincial,
                    nombre_a_cargo_provincial=nombre_a_cargo_provincial
                )

        # Guardar los detalles adicionales para dependencias secundarias
        for dependencia_secundaria in form.cleaned_data['dependencias_secundarias']:
            numero_movil_secundaria = self.request.POST.get(f'numero_movil_secundaria_{dependencia_secundaria.id}')
            nombre_a_cargo_secundaria = self.request.POST.get(f'nombre_a_cargo_secundaria_{dependencia_secundaria.id}')
            if numero_movil_secundaria or nombre_a_cargo_secundaria:
                DetalleDependenciaSecundaria.objects.create(
                    dependencia_secundaria=dependencia_secundaria,
                    comisaria_tercera=self.object,
                    numero_movil_secundaria=numero_movil_secundaria,
                    nombre_a_cargo_secundaria=nombre_a_cargo_secundaria
                )

        # Guardar los detalles adicionales para instituciones federales
        for institucion_federal in form.cleaned_data['instituciones_federales']:
            numero_movil_federal = self.request.POST.get(f'numero_movil_federal_{institucion_federal.id}')
            nombre_a_cargo_federal = self.request.POST.get(f'nombre_a_cargo_federal_{institucion_federal.id}')
            if numero_movil_federal or nombre_a_cargo_federal:
                DetalleInstitucionFederal.objects.create(
                    institucion_federal=institucion_federal,
                    comisaria_tercera=self.object,
                    numero_movil_federal=numero_movil_federal,
                    nombre_a_cargo_federal=nombre_a_cargo_federal
                )

        messages.success(self.request, 'El código ha sido guardado exitosamente.')
        return super().form_valid(form)



#---------------------------------------upadate de comisaria tercera-------------------------------------


class ComisariaTerceraUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ComisariaTercera
    form_class = ComisariaTerceraForm
    template_name = 'comisarias/tercera/comisaria_tercera_form.html'
    success_url = reverse_lazy('comisaria_tercera_list')

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariatercera')

    def handle_no_permission(self):
        return redirect('no_permission')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        now = timezone.now()

        if obj.fecha_hora.date() != now.date() and not obj.estado:
            return redirect('comisaria_tercera_list')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['codigos_policiales'] = CodigoPolicialUSH.objects.all()

        # Convertir detalles en JSON para ser usados por Alpine.js
        context['detalle_servicios_emergencia'] = json.dumps(list(
            DetalleServicioEmergencia.objects.filter(comisaria_tercera=self.object.pk).values('id', 'servicio_emergencia_id', 'numero_movil_bomberos', 'nombre_a_cargo_bomberos')
        ))

        context['detalle_instituciones_hospitalarias'] = json.dumps(list(
            DetalleInstitucionHospitalaria.objects.filter(comisaria_tercera=self.object.pk).values('id', 'institucion_hospitalaria_id', 'numero_movil_hospital', 'nombre_a_cargo_hospital')
        ))

        context['detalle_dependencias_municipales'] = json.dumps(list(
            DetalleDependenciaMunicipal.objects.filter(comisaria_tercera=self.object.pk).values('id', 'dependencia_municipal_id', 'numero_movil_municipal', 'nombre_a_cargo_municipal')
        ))

        context['detalle_dependencias_provinciales'] = json.dumps(list(
            DetalleDependenciaProvincial.objects.filter(comisaria_tercera=self.object.pk).values('id', 'dependencia_provincial_id', 'numero_movil_provincial', 'nombre_a_cargo_provincial')
        ))

        # Añadir los nuevos detalles para dependencias secundarias
        context['detalle_dependencias_secundarias'] = json.dumps(list(
            DetalleDependenciaSecundaria.objects.filter(comisaria_tercera=self.object.pk).values('id', 'dependencia_secundaria_id', 'numero_movil_secundaria', 'nombre_a_cargo_secundaria')
        ))

        # Añadir los nuevos detalles para instituciones federales
        context['detalle_instituciones_federales'] = json.dumps(list(
            DetalleInstitucionFederal.objects.filter(comisaria_tercera=self.object.pk).values('id', 'institucion_federal_id', 'numero_movil_federal', 'nombre_a_cargo_federal')
        ))

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_by = self.request.user
        self.object.updated_at = timezone.now()

        latitude = self.request.POST.get('latitude').replace(',', '.')
        longitude = self.request.POST.get('longitude').replace(',', '.')

        self.object.latitude = float(latitude) if latitude else None
        self.object.longitude = float(longitude) if longitude else None

        self.object.save()
        form.save_m2m()

        # Mantener un registro de los IDs seleccionados
        servicios_emergencia_ids = form.cleaned_data['servicios_emergencia'].values_list('id', flat=True)
        instituciones_hospitalarias_ids = form.cleaned_data['instituciones_hospitalarias'].values_list('id', flat=True)
        dependencias_municipales_ids = form.cleaned_data['dependencias_municipales'].values_list('id', flat=True)
        dependencias_provinciales_ids = form.cleaned_data['dependencias_provinciales'].values_list('id', flat=True)
        dependencias_secundarias_ids = form.cleaned_data['dependencias_secundarias'].values_list('id', flat=True)
        instituciones_federales_ids = form.cleaned_data['instituciones_federales'].values_list('id', flat=True)

        # Eliminar los detalles que ya no están seleccionados
        DetalleServicioEmergencia.objects.filter(comisaria_tercera=self.object).exclude(servicio_emergencia_id__in=servicios_emergencia_ids).delete()
        DetalleInstitucionHospitalaria.objects.filter(comisaria_tercera=self.object).exclude(institucion_hospitalaria_id__in=instituciones_hospitalarias_ids).delete()
        DetalleDependenciaMunicipal.objects.filter(comisaria_tercera=self.object).exclude(dependencia_municipal_id__in=dependencias_municipales_ids).delete()
        DetalleDependenciaProvincial.objects.filter(comisaria_tercera=self.object).exclude(dependencia_provincial_id__in=dependencias_provinciales_ids).delete()
        DetalleDependenciaSecundaria.objects.filter(comisaria_tercera=self.object).exclude(dependencia_secundaria_id__in=dependencias_secundarias_ids).delete()
        DetalleInstitucionFederal.objects.filter(comisaria_tercera=self.object).exclude(institucion_federal_id__in=instituciones_federales_ids).delete()


        # Guardar los detalles adicionales para cada servicio de emergencia.
        for servicio in form.cleaned_data['servicios_emergencia']:
            numero_movil_bomberos = self.request.POST.get(f'numero_movil_bomberos_{servicio.id}')
            nombre_a_cargo_bomberos = self.request.POST.get(f'nombre_a_cargo_bomberos_{servicio.id}')
            DetalleServicioEmergencia.objects.update_or_create(
                servicio_emergencia=servicio,
                comisaria_tercera=self.object,
                defaults={
                    'numero_movil_bomberos': numero_movil_bomberos,
                    'nombre_a_cargo_bomberos': nombre_a_cargo_bomberos
                }
            )

        # Guardar los detalles adicionales para cada institución hospitalaria
        for institucion in form.cleaned_data['instituciones_hospitalarias']:
            numero_movil_hospital = self.request.POST.get(f'numero_movil_hospital_{institucion.id}')
            nombre_a_cargo_hospital = self.request.POST.get(f'nombre_a_cargo_hospital_{institucion.id}')
            DetalleInstitucionHospitalaria.objects.update_or_create(
                institucion_hospitalaria=institucion,
                comisaria_tercera=self.object,
                defaults={
                    'numero_movil_hospital': numero_movil_hospital,
                    'nombre_a_cargo_hospital': nombre_a_cargo_hospital
                }
            )

        # Guardar los detalles adicionales para cada dependencia municipal
        for dependencia_municipal in form.cleaned_data['dependencias_municipales']:
            numero_movil_municipal = self.request.POST.get(f'numero_movil_municipal_{dependencia_municipal.id}')
            nombre_a_cargo_municipal = self.request.POST.get(f'nombre_a_cargo_municipal_{dependencia_municipal.id}')
            DetalleDependenciaMunicipal.objects.update_or_create(
                dependencia_municipal=dependencia_municipal,
                comisaria_tercera=self.object,
                defaults={
                    'numero_movil_municipal': numero_movil_municipal,
                    'nombre_a_cargo_municipal': nombre_a_cargo_municipal
                }
            )

        # Guardar los detalles adicionales para cada dependencia provincial
        for dependencia_provincial in form.cleaned_data['dependencias_provinciales']:
            numero_movil_provincial = self.request.POST.get(f'numero_movil_provincial_{dependencia_provincial.id}')
            nombre_a_cargo_provincial = self.request.POST.get(f'nombre_a_cargo_provincial_{dependencia_provincial.id}')
            DetalleDependenciaProvincial.objects.update_or_create(
                dependencia_provincial=dependencia_provincial,
                comisaria_tercera=self.object,
                defaults={
                    'numero_movil_provincial': numero_movil_provincial,
                    'nombre_a_cargo_provincial': nombre_a_cargo_provincial
                }
            )

        # Guardar detalles adicionales para cada dependencia secundaria
        for dependencia_secundaria in form.cleaned_data['dependencias_secundarias']:
            numero_movil_secundaria = self.request.POST.get(f'numero_movil_secundaria_{dependencia_secundaria.id}')
            nombre_a_cargo_secundaria = self.request.POST.get(f'nombre_a_cargo_secundaria_{dependencia_secundaria.id}')
            DetalleDependenciaSecundaria.objects.update_or_create(
                dependencia_secundaria=dependencia_secundaria,
                comisaria_tercera=self.object,
                defaults={
                    'numero_movil_secundaria': numero_movil_secundaria,
                    'nombre_a_cargo_secundaria': nombre_a_cargo_secundaria
                }
            )

        # Guardar detalles adicionales para instituciones federales
        for institucion_federal in form.cleaned_data['instituciones_federales']:
            numero_movil_federal = self.request.POST.get(f'numero_movil_federal_{institucion_federal.id}')
            nombre_a_cargo_federal = self.request.POST.get(f'nombre_a_cargo_federal_{institucion_federal.id}')
            DetalleInstitucionFederal.objects.update_or_create(
                institucion_federal=institucion_federal,
                comisaria_tercera=self.object,
                defaults={
                    'numero_movil_federal': numero_movil_federal,
                    'nombre_a_cargo_federal': nombre_a_cargo_federal
                }
            )

        messages.success(self.request, 'El código ha sido guardado exitosamente.')
        return super().form_valid(form)


#--------------------------vista para ver todos completo cada registro------------------------------------------------------



class ComisariaTerceraDetailView(DetailView):
    model = ComisariaTercera
    template_name = 'comisarias/tercera/comisaria_tercera_detail.html'
    context_object_name = 'record'


#----------------------------softdelete-------------------------------------------------------------

# En views.py

def eliminar_comisaria_tercera(request, pk):
    # Obtén el registro a eliminar
    comisaria = get_object_or_404(ComisariaTercera, pk=pk)
    
    # Marca el registro como inactivo
    comisaria.activo = False
    comisaria.save()
    
    # Envía un mensaje de confirmación
    messages.success(request, 'El código ha sido eliminado correctamente.')
    
    # Redirige de vuelta a la lista
    return redirect('comisaria_tercera_list')



#--------------------------vista para para la comisria cuarta------------------------------------------------------



class ComisariaCuartaListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ComisariaCuarta
    template_name = 'comisarias/cuarta/comisaria_cuarta_list.html'
    context_object_name = 'records'

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariacuarta')

    def handle_no_permission(self):
        return redirect('no_permission')

    def get_queryset(self):
        queryset = super().get_queryset().filter(activo=True).order_by('-fecha_hora')
        #queryset = super().get_queryset().order_by('-fecha_hora')
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(cuarto__cuarto__icontains=search_query)
        for comisaria in queryset:
            if timezone.is_naive(comisaria.fecha_hora):
                comisaria.fecha_hora = timezone.make_aware(comisaria.fecha_hora, timezone.get_current_timezone())
            comisaria.fecha_hora = timezone.localtime(comisaria.fecha_hora)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['is_jefessuperiores'] = user.groups.filter(name='jefessuperiores').exists()
        context['is_libreros'] = user.groups.filter(name='libreros').exists()
        context['is_encargadosguardias'] = user.groups.filter(name='encargadosguardias').exists()
        context['is_oficialesservicios'] = user.groups.filter(name='oficialesservicios').exists()
        context['is_comisariacuarta'] = user.groups.filter(name='comisariacuarta').exists()

        context['today'] = timezone.now().date()
        context['resolveId'] = None
        return context
    

#----------------------Creacion de comisaria cuarta------------------------------------------------------------

class ComisariaCuartaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ComisariaCuarta
    form_class = ComisariaCuartaForm
    template_name = 'comisarias/cuarta/comisaria_cuarta_form.html'
    success_url = reverse_lazy('comisaria_cuarta_list')

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariacuarta')

    def handle_no_permission(self):
        return redirect('no_permission')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['codigos_policiales'] = CodigoPolicialUSH.objects.all()

        # Inicializar detalles como listas vacías en el contexto
        context['detalle_servicios_emergencia'] = json.dumps([])  # Para vista de creación, siempre es una lista vacía
        context['detalle_instituciones_hospitalarias'] = json.dumps([])
        context['detalle_dependencias_municipales'] = json.dumps([])
        context['detalle_dependencias_provinciales'] = json.dumps([])
        context['detalle_dependencias_secundarias'] = json.dumps([])
        context['detalle_instituciones_federales'] = json.dumps([])  # Añadido para federales

        return context

    def form_valid(self, form): 
        if self.request.POST.get('is_confirmed') == 'true':    
            self.object = form.save(commit=False)
            self.object.created_by = self.request.user
            self.object.updated_by = None
            self.object.updated_at = None

            latitude = self.request.POST.get('latitude').replace(',', '.')
            longitude = self.request.POST.get('longitude').replace(',', '.')

            self.object.latitude = float(latitude) if latitude else None
            self.object.longitude = float(longitude) if longitude else None

            self.object.save()
            form.save_m2m()

            # Guardar los detalles adicionales para cada servicio de emergencia
            for servicio in form.cleaned_data['servicios_emergencia']:
                numero_movil_bomberos = self.request.POST.get(f'numero_movil_bomberos_{servicio.id}')
                nombre_a_cargo_bomberos = self.request.POST.get(f'nombre_a_cargo_bomberos_{servicio.id}')
                if numero_movil_bomberos or nombre_a_cargo_bomberos:
                    DetalleServicioEmergencia.objects.create(
                        servicio_emergencia=servicio,
                        comisaria_cuarta=self.object,
                        numero_movil_bomberos=numero_movil_bomberos,
                        nombre_a_cargo_bomberos=nombre_a_cargo_bomberos
                    )

            # Guardar los detalles adicionales para cada institución hospitalaria
            for institucion in form.cleaned_data['instituciones_hospitalarias']:
                numero_movil_hospital = self.request.POST.get(f'numero_movil_hospital_{institucion.id}')
                nombre_a_cargo_hospital = self.request.POST.get(f'nombre_a_cargo_hospital_{institucion.id}')
                if numero_movil_hospital or nombre_a_cargo_hospital:
                    DetalleInstitucionHospitalaria.objects.create(
                        institucion_hospitalaria=institucion,
                        comisaria_cuarta=self.object,
                        numero_movil_hospital=numero_movil_hospital,
                        nombre_a_cargo_hospital=nombre_a_cargo_hospital
                    )

            # Guardar los detalles adicionales para cada dependencia municipal
            for dependencia_municipal in form.cleaned_data['dependencias_municipales']:
                numero_movil_municipal = self.request.POST.get(f'numero_movil_municipal_{dependencia_municipal.id}')
                nombre_a_cargo_municipal = self.request.POST.get(f'nombre_a_cargo_municipal_{dependencia_municipal.id}')
                if numero_movil_municipal or nombre_a_cargo_municipal:
                    DetalleDependenciaMunicipal.objects.create(
                        dependencia_municipal=dependencia_municipal,
                        comisaria_cuarta=self.object,
                        numero_movil_municipal=numero_movil_municipal,
                        nombre_a_cargo_municipal=nombre_a_cargo_municipal
                    )

            # Guardar los detalles adicionales para cada dependencia provincial
            for dependencia_provincial in form.cleaned_data['dependencias_provinciales']:
                numero_movil_provincial = self.request.POST.get(f'numero_movil_provincial_{dependencia_provincial.id}')
                nombre_a_cargo_provincial = self.request.POST.get(f'nombre_a_cargo_provincial_{dependencia_provincial.id}')
                if numero_movil_provincial or nombre_a_cargo_provincial:
                    DetalleDependenciaProvincial.objects.create(
                        dependencia_provincial=dependencia_provincial,
                        comisaria_cuarta=self.object,
                        numero_movil_provincial=numero_movil_provincial,
                        nombre_a_cargo_provincial=nombre_a_cargo_provincial
                    )

            # Guardar los detalles adicionales para dependencias secundarias
            for dependencia_secundaria in form.cleaned_data['dependencias_secundarias']:
                numero_movil_secundaria = self.request.POST.get(f'numero_movil_secundaria_{dependencia_secundaria.id}')
                nombre_a_cargo_secundaria = self.request.POST.get(f'nombre_a_cargo_secundaria_{dependencia_secundaria.id}')
                if numero_movil_secundaria or nombre_a_cargo_secundaria:
                    DetalleDependenciaSecundaria.objects.create(
                        dependencia_secundaria=dependencia_secundaria,
                        comisaria_cuarta=self.object,
                        numero_movil_secundaria=numero_movil_secundaria,
                        nombre_a_cargo_secundaria=nombre_a_cargo_secundaria
                    )

            # Guardar los detalles adicionales para instituciones federales
            for institucion_federal in form.cleaned_data['instituciones_federales']:
                numero_movil_federal = self.request.POST.get(f'numero_movil_federal_{institucion_federal.id}')
                nombre_a_cargo_federal = self.request.POST.get(f'nombre_a_cargo_federal_{institucion_federal.id}')
                if numero_movil_federal or nombre_a_cargo_federal:
                    DetalleInstitucionFederal.objects.create(
                        institucion_federal=institucion_federal,
                        comisaria_cuarta=self.object,
                        numero_movil_federal=numero_movil_federal,
                        nombre_a_cargo_federal=nombre_a_cargo_federal
                    )

            messages.success(self.request, 'El código ha sido guardado exitosamente.')
            return super().form_valid(form)
        else:
            # Si no ha sido confirmado, mostramos un mensaje de advertencia
            messages.warning(self.request, 'La acción fue cancelada.')
            return redirect('comisaria_cuarta_list')  # Redirigir a la lista u otra página


#--------------------------update comisaria cuarta------------------------------------------------------

class ComisariaCuartaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ComisariaCuarta
    form_class = ComisariaCuartaForm
    template_name = 'comisarias/cuarta/comisaria_cuarta_form.html'
    success_url = reverse_lazy('comisaria_cuarta_list')

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariacuarta')

    def handle_no_permission(self):
        return redirect('no_permission')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        now = timezone.now()

        if obj.fecha_hora.date() != now.date() and not obj.estado:
            return redirect('comisaria_cuarta_list')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['codigos_policiales'] = CodigoPolicialUSH.objects.all()

        # Convertir detalles en JSON para ser usados por Alpine.js
        context['detalle_servicios_emergencia'] = json.dumps(list(
            DetalleServicioEmergencia.objects.filter(comisaria_cuarta=self.object.pk).values('id', 'servicio_emergencia_id', 'numero_movil_bomberos', 'nombre_a_cargo_bomberos')
        ))

        context['detalle_instituciones_hospitalarias'] = json.dumps(list(
            DetalleInstitucionHospitalaria.objects.filter(comisaria_cuarta=self.object.pk).values('id', 'institucion_hospitalaria_id', 'numero_movil_hospital', 'nombre_a_cargo_hospital')
        ))

        context['detalle_dependencias_municipales'] = json.dumps(list(
            DetalleDependenciaMunicipal.objects.filter(comisaria_cuarta=self.object.pk).values('id', 'dependencia_municipal_id', 'numero_movil_municipal', 'nombre_a_cargo_municipal')
        ))

        context['detalle_dependencias_provinciales'] = json.dumps(list(
            DetalleDependenciaProvincial.objects.filter(comisaria_cuarta=self.object.pk).values('id', 'dependencia_provincial_id', 'numero_movil_provincial', 'nombre_a_cargo_provincial')
        ))

        # Añadir los nuevos detalles para dependencias secundarias
        context['detalle_dependencias_secundarias'] = json.dumps(list(
            DetalleDependenciaSecundaria.objects.filter(comisaria_cuarta=self.object.pk).values('id', 'dependencia_secundaria_id', 'numero_movil_secundaria', 'nombre_a_cargo_secundaria')
        ))

        # Añadir los nuevos detalles para instituciones federales
        context['detalle_instituciones_federales'] = json.dumps(list(
            DetalleInstitucionFederal.objects.filter(comisaria_cuarta=self.object.pk).values('id', 'institucion_federal_id', 'numero_movil_federal', 'nombre_a_cargo_federal')
        ))

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_by = self.request.user
        self.object.updated_at = timezone.now()

        latitude = self.request.POST.get('latitude').replace(',', '.')
        longitude = self.request.POST.get('longitude').replace(',', '.')

        self.object.latitude = float(latitude) if latitude else None
        self.object.longitude = float(longitude) if longitude else None

        self.object.save()
        form.save_m2m()

        # Mantener un registro de los IDs seleccionados
        servicios_emergencia_ids = form.cleaned_data['servicios_emergencia'].values_list('id', flat=True)
        instituciones_hospitalarias_ids = form.cleaned_data['instituciones_hospitalarias'].values_list('id', flat=True)
        dependencias_municipales_ids = form.cleaned_data['dependencias_municipales'].values_list('id', flat=True)
        dependencias_provinciales_ids = form.cleaned_data['dependencias_provinciales'].values_list('id', flat=True)
        dependencias_secundarias_ids = form.cleaned_data['dependencias_secundarias'].values_list('id', flat=True)
        instituciones_federales_ids = form.cleaned_data['instituciones_federales'].values_list('id', flat=True)
        

        # Eliminar los detalles que ya no están seleccionados
        DetalleServicioEmergencia.objects.filter(comisaria_cuarta=self.object).exclude(servicio_emergencia_id__in=servicios_emergencia_ids).delete()
        DetalleInstitucionHospitalaria.objects.filter(comisaria_cuarta=self.object).exclude(institucion_hospitalaria_id__in=instituciones_hospitalarias_ids).delete()
        DetalleDependenciaMunicipal.objects.filter(comisaria_cuarta=self.object).exclude(dependencia_municipal_id__in=dependencias_municipales_ids).delete()
        DetalleDependenciaProvincial.objects.filter(comisaria_cuarta=self.object).exclude(dependencia_provincial_id__in=dependencias_provinciales_ids).delete()
        DetalleDependenciaSecundaria.objects.filter(comisaria_cuarta=self.object).exclude(dependencia_secundaria_id__in=dependencias_secundarias_ids).delete()
        DetalleInstitucionFederal.objects.filter(comisaria_cuarta=self.object).exclude(institucion_federal_id__in=instituciones_federales_ids).delete()
        

        # Guardar los detalles adicionales para cada servicio de emergencia.
        for servicio in form.cleaned_data['servicios_emergencia']:
            numero_movil_bomberos = self.request.POST.get(f'numero_movil_bomberos_{servicio.id}')
            nombre_a_cargo_bomberos = self.request.POST.get(f'nombre_a_cargo_bomberos_{servicio.id}')
            DetalleServicioEmergencia.objects.update_or_create(
                servicio_emergencia=servicio,
                comisaria_cuarta=self.object,
                defaults={
                    'numero_movil_bomberos': numero_movil_bomberos,
                    'nombre_a_cargo_bomberos': nombre_a_cargo_bomberos
                }
            )

        # Guardar los detalles adicionales para cada institución hospitalaria
        for institucion in form.cleaned_data['instituciones_hospitalarias']:
            numero_movil_hospital = self.request.POST.get(f'numero_movil_hospital_{institucion.id}')
            nombre_a_cargo_hospital = self.request.POST.get(f'nombre_a_cargo_hospital_{institucion.id}')
            DetalleInstitucionHospitalaria.objects.update_or_create(
                institucion_hospitalaria=institucion,
                comisaria_cuarta=self.object,
                defaults={
                    'numero_movil_hospital': numero_movil_hospital,
                    'nombre_a_cargo_hospital': nombre_a_cargo_hospital
                }
            )

        # Guardar los detalles adicionales para cada dependencia municipal
        for dependencia_municipal in form.cleaned_data['dependencias_municipales']:
            numero_movil_municipal = self.request.POST.get(f'numero_movil_municipal_{dependencia_municipal.id}')
            nombre_a_cargo_municipal = self.request.POST.get(f'nombre_a_cargo_municipal_{dependencia_municipal.id}')
            DetalleDependenciaMunicipal.objects.update_or_create(
                dependencia_municipal=dependencia_municipal,
                comisaria_cuarta=self.object,
                defaults={
                    'numero_movil_municipal': numero_movil_municipal,
                    'nombre_a_cargo_municipal': nombre_a_cargo_municipal
                }
            )

        # Guardar los detalles adicionales para cada dependencia provincial
        for dependencia_provincial in form.cleaned_data['dependencias_provinciales']:
            numero_movil_provincial = self.request.POST.get(f'numero_movil_provincial_{dependencia_provincial.id}')
            nombre_a_cargo_provincial = self.request.POST.get(f'nombre_a_cargo_provincial_{dependencia_provincial.id}')
            DetalleDependenciaProvincial.objects.update_or_create(
                dependencia_provincial=dependencia_provincial,
                comisaria_cuarta=self.object,
                defaults={
                    'numero_movil_provincial': numero_movil_provincial,
                    'nombre_a_cargo_provincial': nombre_a_cargo_provincial
                }
            )

        # Guardar detalles adicionales para cada dependencia secundaria
        for dependencia_secundaria in form.cleaned_data['dependencias_secundarias']:
            numero_movil_secundaria = self.request.POST.get(f'numero_movil_secundaria_{dependencia_secundaria.id}')
            nombre_a_cargo_secundaria = self.request.POST.get(f'nombre_a_cargo_secundaria_{dependencia_secundaria.id}')
            DetalleDependenciaSecundaria.objects.update_or_create(
                dependencia_secundaria=dependencia_secundaria,
                comisaria_cuarta=self.object,
                defaults={
                    'numero_movil_secundaria': numero_movil_secundaria,
                    'nombre_a_cargo_secundaria': nombre_a_cargo_secundaria
                }
            )

        # Guardar detalles adicionales para instituciones federales
        for institucion_federal in form.cleaned_data['instituciones_federales']:
            numero_movil_federal = self.request.POST.get(f'numero_movil_federal_{institucion_federal.id}')
            nombre_a_cargo_federal = self.request.POST.get(f'nombre_a_cargo_federal_{institucion_federal.id}')
            DetalleInstitucionFederal.objects.update_or_create(
                institucion_federal=institucion_federal,
                comisaria_cuarta=self.object,
                defaults={
                    'numero_movil_federal': numero_movil_federal,
                    'nombre_a_cargo_federal': nombre_a_cargo_federal
                }
            )

        messages.success(self.request, 'El código ha sido guardado exitosamente.')
        return super().form_valid(form)


#---------------------detalle de comisaria cuarta-----------------------------------------------

class ComisariaCuartaDetailView(DetailView):
    model = ComisariaCuarta
    template_name = 'comisarias/cuarta/comisaria_cuarta_detail.html'
    context_object_name = 'record'


#----------------------------softdelete-------------------------------------------------------------

# En views.py

def eliminar_comisaria_cuarta(request, pk):
    # Obtén el registro a eliminar
    comisaria = get_object_or_404(ComisariaCuarta, pk=pk)
    
    # Marca el registro como inactivo
    comisaria.activo = False
    comisaria.save()
    
    # Envía un mensaje de confirmación
    messages.success(request, 'El código ha sido eliminado correctamente.')
    
    # Redirige de vuelta a la lista
    return redirect('comisaria_cuarta_list')





#---------------------comisaria quinta para ver ---------------------

class ComisariaQuintaListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ComisariaQuinta
    template_name = 'comisarias/quinta/comisaria_quinta_list.html'
    context_object_name = 'records'

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariaquinta')

    def handle_no_permission(self):
        return redirect('no_permission')

    def get_queryset(self):
        queryset = super().get_queryset().filter(activo=True).order_by('-fecha_hora')
        #queryset = super().get_queryset().order_by('-fecha_hora')
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(cuarto__cuarto__icontains=search_query)
        for comisaria in queryset:
            if timezone.is_naive(comisaria.fecha_hora):
                comisaria.fecha_hora = timezone.make_aware(comisaria.fecha_hora, timezone.get_current_timezone())
            comisaria.fecha_hora = timezone.localtime(comisaria.fecha_hora)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['is_jefessuperiores'] = user.groups.filter(name='jefessuperiores').exists()
        context['is_libreros'] = user.groups.filter(name='libreros').exists()
        context['is_encargadosguardias'] = user.groups.filter(name='encargadosguardias').exists()
        context['is_oficialesservicios'] = user.groups.filter(name='oficialesservicios').exists()
        context['is_comisariaquinta'] = user.groups.filter(name='comisariaquinta').exists()

        context['today'] = timezone.now().date()
        context['resolveId'] = None
        return context


#-----------------------creacion de comisaria quinta---------------

class ComisariaQuintaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ComisariaQuinta
    form_class = ComisariaQuintaForm
    template_name = 'comisarias/quinta/comisaria_quinta_form.html'
    success_url = reverse_lazy('comisaria_quinta_list')

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariaquinta')

    def handle_no_permission(self):
        return redirect('no_permission')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['codigos_policiales'] = CodigoPolicialUSH.objects.all()

        # Inicializar detalles como listas vacías en el contexto
        context['detalle_servicios_emergencia'] = json.dumps([])  # Para vista de creación, siempre es una lista vacía
        context['detalle_instituciones_hospitalarias'] = json.dumps([])
        context['detalle_dependencias_municipales'] = json.dumps([])
        context['detalle_dependencias_provinciales'] = json.dumps([])
        context['detalle_dependencias_secundarias'] = json.dumps([])
        context['detalle_instituciones_federales'] = json.dumps([])  # Añadido para federales

        return context

    def form_valid(self, form):
        if self.request.POST.get('is_confirmed') == 'true': 
            self.object = form.save(commit=False)
            self.object.created_by = self.request.user
            self.object.updated_by = None
            self.object.updated_at = None

            latitude = self.request.POST.get('latitude').replace(',', '.')
            longitude = self.request.POST.get('longitude').replace(',', '.')

            self.object.latitude = float(latitude) if latitude else None
            self.object.longitude = float(longitude) if longitude else None

            self.object.save()
            form.save_m2m()

            # Guardar los detalles adicionales para cada servicio de emergencia
            for servicio in form.cleaned_data['servicios_emergencia']:
                numero_movil_bomberos = self.request.POST.get(f'numero_movil_bomberos_{servicio.id}')
                nombre_a_cargo_bomberos = self.request.POST.get(f'nombre_a_cargo_bomberos_{servicio.id}')
                if numero_movil_bomberos or nombre_a_cargo_bomberos:
                    DetalleServicioEmergencia.objects.create(
                        servicio_emergencia=servicio,
                        comisaria_quinta=self.object,
                        numero_movil_bomberos=numero_movil_bomberos,
                        nombre_a_cargo_bomberos=nombre_a_cargo_bomberos
                    )

            # Guardar los detalles adicionales para cada institución hospitalaria
            for institucion in form.cleaned_data['instituciones_hospitalarias']:
                numero_movil_hospital = self.request.POST.get(f'numero_movil_hospital_{institucion.id}')
                nombre_a_cargo_hospital = self.request.POST.get(f'nombre_a_cargo_hospital_{institucion.id}')
                if numero_movil_hospital or nombre_a_cargo_hospital:
                    DetalleInstitucionHospitalaria.objects.create(
                        institucion_hospitalaria=institucion,
                        comisaria_quinta=self.object,
                        numero_movil_hospital=numero_movil_hospital,
                        nombre_a_cargo_hospital=nombre_a_cargo_hospital
                    )

            # Guardar los detalles adicionales para cada dependencia municipal
            for dependencia_municipal in form.cleaned_data['dependencias_municipales']:
                numero_movil_municipal = self.request.POST.get(f'numero_movil_municipal_{dependencia_municipal.id}')
                nombre_a_cargo_municipal = self.request.POST.get(f'nombre_a_cargo_municipal_{dependencia_municipal.id}')
                if numero_movil_municipal or nombre_a_cargo_municipal:
                    DetalleDependenciaMunicipal.objects.create(
                        dependencia_municipal=dependencia_municipal,
                        comisaria_quinta=self.object,
                        numero_movil_municipal=numero_movil_municipal,
                        nombre_a_cargo_municipal=nombre_a_cargo_municipal
                    )

            # Guardar los detalles adicionales para cada dependencia provincial
            for dependencia_provincial in form.cleaned_data['dependencias_provinciales']:
                numero_movil_provincial = self.request.POST.get(f'numero_movil_provincial_{dependencia_provincial.id}')
                nombre_a_cargo_provincial = self.request.POST.get(f'nombre_a_cargo_provincial_{dependencia_provincial.id}')
                if numero_movil_provincial or nombre_a_cargo_provincial:
                    DetalleDependenciaProvincial.objects.create(
                        dependencia_provincial=dependencia_provincial,
                        comisaria_quinta=self.object,
                        numero_movil_provincial=numero_movil_provincial,
                        nombre_a_cargo_provincial=nombre_a_cargo_provincial
                    )

            # Guardar los detalles adicionales para dependencias secundarias
            for dependencia_secundaria in form.cleaned_data['dependencias_secundarias']:
                numero_movil_secundaria = self.request.POST.get(f'numero_movil_secundaria_{dependencia_secundaria.id}')
                nombre_a_cargo_secundaria = self.request.POST.get(f'nombre_a_cargo_secundaria_{dependencia_secundaria.id}')
                if numero_movil_secundaria or nombre_a_cargo_secundaria:
                    DetalleDependenciaSecundaria.objects.create(
                        dependencia_secundaria=dependencia_secundaria,
                        comisaria_quinta=self.object,
                        numero_movil_secundaria=numero_movil_secundaria,
                        nombre_a_cargo_secundaria=nombre_a_cargo_secundaria
                    )

            # Guardar los detalles adicionales para instituciones federales
            for institucion_federal in form.cleaned_data['instituciones_federales']:
                numero_movil_federal = self.request.POST.get(f'numero_movil_federal_{institucion_federal.id}')
                nombre_a_cargo_federal = self.request.POST.get(f'nombre_a_cargo_federal_{institucion_federal.id}')
                if numero_movil_federal or nombre_a_cargo_federal:
                    DetalleInstitucionFederal.objects.create(
                        institucion_federal=institucion_federal,
                        comisaria_quinta=self.object,
                        numero_movil_federal=numero_movil_federal,
                        nombre_a_cargo_federal=nombre_a_cargo_federal
                    )

            messages.success(self.request, 'El código ha sido guardado exitosamente.')
            return super().form_valid(form)
        else:
            # Si no ha sido confirmado, mostramos un mensaje de advertencia
            messages.warning(self.request, 'La acción fue cancelada.')
            return redirect('comisaria_cuarta_list')  # Redirigir a la lista u otra página

#-------------------update de comisaria quinta-----------------------------

class ComisariaQuintaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ComisariaQuinta
    form_class = ComisariaQuintaForm
    template_name = 'comisarias/quinta/comisaria_quinta_form.html'
    success_url = reverse_lazy('comisaria_quinta_list')

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariaquinta')

    def handle_no_permission(self):
        return redirect('no_permission')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        now = timezone.now()

        if obj.fecha_hora.date() != now.date() and not obj.estado:
            return redirect('comisaria_quinta_list')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['codigos_policiales'] = CodigoPolicialUSH.objects.all()

        # Convertir detalles en JSON para ser usados por Alpine.js
        context['detalle_servicios_emergencia'] = json.dumps(list(
            DetalleServicioEmergencia.objects.filter(comisaria_quinta=self.object.pk).values('id', 'servicio_emergencia_id', 'numero_movil_bomberos', 'nombre_a_cargo_bomberos')
        ))

        context['detalle_instituciones_hospitalarias'] = json.dumps(list(
            DetalleInstitucionHospitalaria.objects.filter(comisaria_quinta=self.object.pk).values('id', 'institucion_hospitalaria_id', 'numero_movil_hospital', 'nombre_a_cargo_hospital')
        ))

        context['detalle_dependencias_municipales'] = json.dumps(list(
            DetalleDependenciaMunicipal.objects.filter(comisaria_quinta=self.object.pk).values('id', 'dependencia_municipal_id', 'numero_movil_municipal', 'nombre_a_cargo_municipal')
        ))

        context['detalle_dependencias_provinciales'] = json.dumps(list(
            DetalleDependenciaProvincial.objects.filter(comisaria_quinta=self.object.pk).values('id', 'dependencia_provincial_id', 'numero_movil_provincial', 'nombre_a_cargo_provincial')
        ))

        # Añadir los nuevos detalles para dependencias secundarias
        context['detalle_dependencias_secundarias'] = json.dumps(list(
            DetalleDependenciaSecundaria.objects.filter(comisaria_quinta=self.object.pk).values('id', 'dependencia_secundaria_id', 'numero_movil_secundaria', 'nombre_a_cargo_secundaria')
        ))

        # Añadir los nuevos detalles para instituciones federales
        context['detalle_instituciones_federales'] = json.dumps(list(
            DetalleInstitucionFederal.objects.filter(comisaria_quinta=self.object.pk).values('id', 'institucion_federal_id', 'numero_movil_federal', 'nombre_a_cargo_federal')
        ))

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_by = self.request.user
        self.object.updated_at = timezone.now()

        latitude = self.request.POST.get('latitude').replace(',', '.')
        longitude = self.request.POST.get('longitude').replace(',', '.')

        self.object.latitude = float(latitude) if latitude else None
        self.object.longitude = float(longitude) if longitude else None

        self.object.save()
        form.save_m2m()

       # Mantener un registro de los IDs seleccionados
        servicios_emergencia_ids = form.cleaned_data['servicios_emergencia'].values_list('id', flat=True)
        instituciones_hospitalarias_ids = form.cleaned_data['instituciones_hospitalarias'].values_list('id', flat=True)
        dependencias_municipales_ids = form.cleaned_data['dependencias_municipales'].values_list('id', flat=True)
        dependencias_provinciales_ids = form.cleaned_data['dependencias_provinciales'].values_list('id', flat=True)
        dependencias_secundarias_ids = form.cleaned_data['dependencias_secundarias'].values_list('id', flat=True)
        instituciones_federales_ids = form.cleaned_data['instituciones_federales'].values_list('id', flat=True)

        # Eliminar los detalles que ya no están seleccionados
        DetalleServicioEmergencia.objects.filter(comisaria_quinta=self.object).exclude(servicio_emergencia_id__in=servicios_emergencia_ids).delete()
        DetalleInstitucionHospitalaria.objects.filter(comisaria_quinta=self.object).exclude(institucion_hospitalaria_id__in=instituciones_hospitalarias_ids).delete()
        DetalleDependenciaMunicipal.objects.filter(comisaria_quinta=self.object).exclude(dependencia_municipal_id__in=dependencias_municipales_ids).delete()
        DetalleDependenciaProvincial.objects.filter(comisaria_quinta=self.object).exclude(dependencia_provincial_id__in=dependencias_provinciales_ids).delete()
        DetalleDependenciaSecundaria.objects.filter(comisaria_quinta=self.object).exclude(dependencia_secundaria_id__in=dependencias_secundarias_ids).delete()
        DetalleInstitucionFederal.objects.filter(comisaria_quinta=self.object).exclude(institucion_federal_id__in=instituciones_federales_ids).delete()

        # Guardar los detalles adicionales para cada servicio de emergencia
        for servicio in form.cleaned_data['servicios_emergencia']:
            numero_movil_bomberos = self.request.POST.get(f'numero_movil_bomberos_{servicio.id}')
            nombre_a_cargo_bomberos = self.request.POST.get(f'nombre_a_cargo_bomberos_{servicio.id}')
            DetalleServicioEmergencia.objects.update_or_create(
                servicio_emergencia=servicio,
                comisaria_quinta=self.object,
                defaults={
                    'numero_movil_bomberos': numero_movil_bomberos,
                    'nombre_a_cargo_bomberos': nombre_a_cargo_bomberos
                }
            )

        # Guardar los detalles adicionales para cada institución hospitalaria
        for institucion in form.cleaned_data['instituciones_hospitalarias']:
            numero_movil_hospital = self.request.POST.get(f'numero_movil_hospital_{institucion.id}')
            nombre_a_cargo_hospital = self.request.POST.get(f'nombre_a_cargo_hospital_{institucion.id}')
            DetalleInstitucionHospitalaria.objects.update_or_create(
                institucion_hospitalaria=institucion,
                comisaria_quinta=self.object,
                defaults={
                    'numero_movil_hospital': numero_movil_hospital,
                    'nombre_a_cargo_hospital': nombre_a_cargo_hospital
                }
            )

        # Guardar los detalles adicionales para cada dependencia municipal
        for dependencia_municipal in form.cleaned_data['dependencias_municipales']:
            numero_movil_municipal = self.request.POST.get(f'numero_movil_municipal_{dependencia_municipal.id}')
            nombre_a_cargo_municipal = self.request.POST.get(f'nombre_a_cargo_municipal_{dependencia_municipal.id}')
            DetalleDependenciaMunicipal.objects.update_or_create(
                dependencia_municipal=dependencia_municipal,
                comisaria_quinta=self.object,
                defaults={
                    'numero_movil_municipal': numero_movil_municipal,
                    'nombre_a_cargo_municipal': nombre_a_cargo_municipal
                }
            )

        # Guardar los detalles adicionales para cada dependencia provincial
        for dependencia_provincial in form.cleaned_data['dependencias_provinciales']:
            numero_movil_provincial = self.request.POST.get(f'numero_movil_provincial_{dependencia_provincial.id}')
            nombre_a_cargo_provincial = self.request.POST.get(f'nombre_a_cargo_provincial_{dependencia_provincial.id}')
            DetalleDependenciaProvincial.objects.update_or_create(
                dependencia_provincial=dependencia_provincial,
                comisaria_quinta=self.object,
                defaults={
                    'numero_movil_provincial': numero_movil_provincial,
                    'nombre_a_cargo_provincial': nombre_a_cargo_provincial
                }
            )

        # Guardar los detalles adicionales para dependencias secundarias
        for dependencia_secundaria in form.cleaned_data['dependencias_secundarias']:
            numero_movil_secundaria = self.request.POST.get(f'numero_movil_secundaria_{dependencia_secundaria.id}')
            nombre_a_cargo_secundaria = self.request.POST.get(f'nombre_a_cargo_secundaria_{dependencia_secundaria.id}')
            DetalleDependenciaSecundaria.objects.update_or_create(
                dependencia_secundaria=dependencia_secundaria,
                comisaria_quinta=self.object,
                defaults={
                    'numero_movil_secundaria': numero_movil_secundaria,
                    'nombre_a_cargo_secundaria': nombre_a_cargo_secundaria
                }
            )

        # Guardar los detalles adicionales para instituciones federales
        for institucion_federal in form.cleaned_data['instituciones_federales']:
            numero_movil_federal = self.request.POST.get(f'numero_movil_federal_{institucion_federal.id}')
            nombre_a_cargo_federal = self.request.POST.get(f'nombre_a_cargo_federal_{institucion_federal.id}')
            DetalleInstitucionFederal.objects.update_or_create(
                institucion_federal=institucion_federal,
                comisaria_quinta=self.object,
                defaults={
                    'numero_movil_federal': numero_movil_federal,
                    'nombre_a_cargo_federal': nombre_a_cargo_federal
                }
            )

        messages.success(self.request, 'El código ha sido guardado exitosamente.')

        return super().form_valid(form)
    

#--------------------detalle comisria quinta---------------------------------------------


class ComisariaQuintaDetailView(DetailView):
    model = ComisariaQuinta
    template_name = 'comisarias/quinta/comisaria_quinta_detail.html'
    context_object_name = 'record'


#----------------------------softdelete-------------------------------------------------------------

# En views.py

def eliminar_comisaria_quinta(request, pk):
    # Obtén el registro a eliminar
    comisaria = get_object_or_404(ComisariaQuinta, pk=pk)
    
    # Marca el registro como inactivo
    comisaria.activo = False
    comisaria.save()
    
    # Envía un mensaje de confirmación
    messages.success(request, 'El código ha sido eliminado correctamente.')
    
    # Redirige de vuelta a la lista
    return redirect('comisaria_quinta_list')



#--------------------vista dee todas las comisarias-------------------------------------    

from django.db.models import Value, Q, CharField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class ComisariasCompletaListView(LoginRequiredMixin, ListView):
    template_name = 'comisarias/comisarias_completa_list.html'
    context_object_name = 'page_obj'

    def get_paginate_by(self, queryset):
        """Define el número de registros por página dinámicamente."""
        items_per_page = self.request.GET.get('items_per_page', 10)
        try:
            return int(items_per_page)
        except ValueError:
            return 10  # Valor por defecto si no es válido

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()  # Obtiene y limpia la consulta

        # Crea un filtro Q común para reutilizarlo
        search_filter = (
            Q(comisaria_nombre__icontains=query) |
            Q(cuarto__cuarto__icontains=query) |
            Q(codigo__codigo__icontains=query) |
            Q(codigo__nombre_codigo__icontains=query) |
            Q(movil_patrulla__icontains=query) |
            Q(a_cargo__icontains=query) |
            Q(secundante__icontains=query) |
            Q(lugar_codigo__icontains=query) |
            Q(tareas_judiciales__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(fecha_hora__icontains=query)
        ) if query else Q()  # Solo aplica el filtro si hay una consulta

        # Filtra y anota cada QuerySet individualmente
        comisarias_primera = ComisariaPrimera.objects.filter(
            activo=True
        ).select_related('cuarto').annotate(
            comisaria_nombre=Value('Comisaria Primera', output_field=CharField())
        ).filter(search_filter)

        comisarias_segunda = ComisariaSegunda.objects.filter(
            activo=True
        ).select_related('cuarto').annotate(
            comisaria_nombre=Value('Comisaria Segunda', output_field=CharField())
        ).filter(search_filter)

        comisarias_tercera = ComisariaTercera.objects.filter(
            activo=True
        ).select_related('cuarto').annotate(
            comisaria_nombre=Value('Comisaria Tercera', output_field=CharField())
        ).filter(search_filter)

        comisarias_cuarta = ComisariaCuarta.objects.filter(
            activo=True
        ).select_related('cuarto').annotate(
            comisaria_nombre=Value('Comisaria Cuarta', output_field=CharField())
        ).filter(search_filter)

        comisarias_quinta = ComisariaQuinta.objects.filter(
            activo=True
        ).select_related('cuarto').annotate(
            comisaria_nombre=Value('Comisaria Quinta', output_field=CharField())
        ).filter(search_filter)

        # Unión de los QuerySets
        combined_queryset = comisarias_primera.union(
            comisarias_segunda,
            comisarias_tercera,
            comisarias_cuarta,
            comisarias_quinta
        )

        # Ordenar por fecha de creación
        return combined_queryset.order_by('-created_at')
    
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

    # Paginación
        paginate_by = self.get_paginate_by(queryset)
        paginator = Paginator(queryset, paginate_by)
        page = self.request.GET.get('page')

        try:
           page_obj = paginator.page(page)
        except PageNotAnInteger:
           page_obj = paginator.page(1)
        except EmptyPage:
           page_obj = paginator.page(paginator.num_pages)

    # Calcular el rango dinámico de páginas
        current_page = page_obj.number
        total_pages = page_obj.paginator.num_pages
        range_start = max(current_page - 5, 1)
        range_end = min(current_page + 5, total_pages) + 1  # Incluye la última página

        context['page_obj'] = page_obj
        context['query'] = self.request.GET.get('q', '')
        context['items_per_page'] = paginate_by
        context['page_range'] = range(range_start, range_end)
        return context




        



#-------------------------------genera pdf para firma y descarga------------------------------------------------------

def generate_pdf_content(request, comisaria_model, add_signature=False):
    # 1. Obtener la fecha y hora actual
    now = datetime.now()

    # 2. Definir el inicio y el fin del día actual
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    # 3. Filtrar los registros del modelo de la comisaría según las fechas de creación o actualización del día actual
    registros = comisaria_model.objects.filter(
        models.Q(created_at__range=(start_of_day, end_of_day)) |
        models.Q(updated_at__range=(start_of_day, end_of_day)),
        activo=True  # Filtrar solo los registros activos
    )

    # 4. Cargar la plantilla HTML que se usará para generar el PDF
    template = get_template('comisarias/comisarias_pdf_template.html')

    
    # Convierte la imagen a base64
    escudo_path = os.path.join(settings.BASE_DIR, 'comisarias', 'static', 'comisarias', 'images', 'ESCUDO POLICIA.jpeg')
    with open(escudo_path, "rb") as img_file:
        escudo_base64 = base64.b64encode(img_file.read()).decode('utf-8')
    

    # 5. Preparar el contexto que se pasará a la plantilla
    context = {
        'registros': registros,  # Los registros filtrados del día
        'comisaria_name': comisaria_model._meta.verbose_name.title(),  # Nombre legible de la comisaría
        'add_signature': add_signature,  # Indicador de si se debe agregar la firma
        'username': request.user.get_full_name(),  # Nombre completo del usuario que genera el PDF
        'now': now,  # Fecha y hora actual
        'escudo_base64': escudo_base64,  # Pasar la imagen en base64 al contexto
       
    }

    # 6. Renderizar la plantilla HTML con el contexto proporcionado
    html = template.render(context)

    # 7. Crear un buffer en memoria para el PDF
    response = BytesIO()

    # 8. Generar el PDF a partir del HTML renderizado
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)

    # 9. Verificar si la generación del PDF fue exitosa
    if not pdf.err:
        # 10. Retornar el contenido del PDF si no hubo errores
        return response.getvalue()
    else:
        # 11. Retornar None si hubo un error en la generación del PDF
        return None
#-------------------------------esta funcion depende de generate_pdf_content----------------------------------------------------------

def generate_pdf(request, comisaria_model, filename, add_signature=False):
    # Llama a la función generate_pdf_content para generar el contenido del PDF.
    # Si la generación es exitosa, pdf_content contendrá los datos binarios del PDF.
    pdf_content = generate_pdf_content(request, comisaria_model, add_signature)
    
    # Verifica si el PDF se generó correctamente (es decir, si pdf_content no es None).
    if pdf_content:
        # Crea una respuesta HTTP con el contenido del PDF y establece el tipo de contenido como 'application/pdf'.
        response = HttpResponse(pdf_content, content_type='application/pdf')
        
        # Establece el encabezado 'Content-Disposition' para mostrar el PDF en el navegador
        # y sugiere un nombre de archivo para la descarga.
        response['Content-Disposition'] = f'inline; filename="{filename}"'
        
        # Devuelve la respuesta HTTP que contiene el PDF.
        return response
    else:
        # Si la generación del PDF falló, devuelve una respuesta HTTP con un mensaje de error
        # y un estado HTTP 500 (Internal Server Error).
        return HttpResponse('Error al generar el PDF', status=500)
    
#---------------------------------------esta funcion depende de generate_pdf_content----------------------------------------------    

def view_pdf_content(request, comisaria_model):
    # Llama a la función generate_pdf_content para generar el contenido del PDF.
    # El contenido se almacena en un buffer de memoria.
    buffer = generate_pdf_content(request, comisaria_model)
    
    # Crea una respuesta de archivo con el contenido del PDF (almacenado en el buffer) y
    # establece el tipo de contenido como 'application/pdf'.
    response = FileResponse(BytesIO(buffer), content_type='application/pdf')
    
    # Devuelve la respuesta HTTP que contiene el PDF, lo que hará que el navegador lo muestre.
    return response

#---------------------------esta funcion retorna el view_pdf_content ---------------------------------------------------


def generate_comisaria_primera_pdf_view(request):
    # Llama a la función view_pdf_content, pasando el request y el modelo ComisariaPrimera.
    # Esta función generará el contenido del PDF para la ComisariaPrimera y lo devolverá como una respuesta HTTP.
    return view_pdf_content(request, ComisariaPrimera)

#-------------------------------esta funcion retorna la funcion generate_pdf-----------------------------------------------------

def generate_comisaria_primera_pdf_download(request):
    
    force_download = request.GET.get('force', 'false') == 'true'
    # Verificar si hay registros con estado activo
    registros_activos = ComisariaPrimera.objects.filter(estado=True, activo=True).exists()

    if registros_activos and not force_download:
        # Retornar una respuesta JSON indicando que hay registros activos
        return JsonResponse({'warning': 'Existen registros con el estado "Activo". ¿Deseas continuar con la descarga del PDF?'})
    
    # Verifica si la URL contiene el parámetro 'signature' en la cadena de consulta (GET).
    # Si está presente, add_signature será True; de lo contrario, será False.
    add_signature = 'signature' in request.GET
    
    # Obtiene la fecha y hora actual.
    now = datetime.now()

    # Obtiene el nombre de la comisaría desde el modelo (por ejemplo, "Comisaria Primera").
    comisaria_name = ComisariaPrimera._meta.verbose_name.title().replace(' ', '-')
    
    # Define el nombre del archivo, incluyendo "libro-diario", el nombre de la comisaría, y la fecha actual.
    filename = f"libro-diario-{comisaria_name}-Ush-{now.strftime('%d-%m-%Y')}.pdf"
    
    # Llama a la función generate_pdf, pasando el request, el modelo ComisariaPrimera, 
    # el nombre de archivo y el valor de add_signature. Esta función generará y devolverá
    # el PDF como una respuesta HTTP para su descarga o visualización.
    return generate_pdf(request, ComisariaPrimera, filename, add_signature=add_signature)

#----------------------------esta funcion descacrga el pdf del dia enterior----------------------------------------------------------------


# Función para descargar el PDF del día anterior
def generate_comisaria_primera_pdf_download_previous_day(request):
    # Verifica si la URL contiene el parámetro 'signature' en la cadena de consulta (GET).
    add_signature = 'signature' in request.GET
    
    # Obtiene la fecha y hora actual.
    now = datetime.now()

    # Obtiene el nombre de la comisaría desde el modelo (por ejemplo, "Comisaria Primera").
    comisaria_name = ComisariaPrimera._meta.verbose_name.title().replace(' ', '-')
    
    
    # Calcula la fecha del día anterior.
    previous_day = now - timedelta(days=1)
    
    # Define el nombre del archivo para el PDF, incluyendo "parte-diario", 
    # la fecha del día anterior, y la extensión ".pdf".
    filename = f"libro-diario-{comisaria_name}-Ush-{previous_day.strftime('%d-%m-%Y')}.pdf"
    
    # Llama a la función generate_pdf_for_specific_date, pasando el request, 
    # el modelo ComisariaPrimera, la fecha del día anterior, el nombre del archivo,
    # y el valor de add_signature. Esta función generará el PDF para la fecha específica
    # y lo devolverá como una respuesta HTTP.
    return generate_pdf_for_specific_date(request, ComisariaPrimera, previous_day, filename, add_signature=add_signature)

#--------------------------------------------------------------------------------------------------------------------------------------

# Función para generar un PDF para una fecha específica
def generate_pdf_for_specific_date(request, comisaria_model, specific_date, filename, add_signature=False):
    # Define el inicio del día específico (00:00:00.000).
    start_of_day = specific_date.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Define el fin del día específico (23:59:59.999).
    end_of_day = specific_date.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    # Filtra los registros de la comisaría para la fecha específica, seleccionando
    # aquellos que fueron creados o actualizados dentro del rango del día.
    registros = comisaria_model.objects.filter(
        models.Q(created_at__range=(start_of_day, end_of_day)) |
        models.Q(updated_at__range=(start_of_day, end_of_day))
    )

    # Carga la plantilla HTML que se utilizará para renderizar el PDF.
    template = get_template('comisarias/comisarias_pdf_template.html')
    
    # Convierte la imagen a base64
    escudo_path = os.path.join(settings.BASE_DIR, 'comisarias', 'static', 'comisarias', 'images', 'ESCUDO POLICIA.jpeg')
    with open(escudo_path, "rb") as img_file:
        escudo_base64 = base64.b64encode(img_file.read()).decode('utf-8')
    
    # Crea un diccionario de contexto con los datos necesarios para renderizar la plantilla HTML.
    context = {
        'registros': registros,
        'comisaria_name': comisaria_model._meta.verbose_name.title(),
        'add_signature': add_signature,
        'username': request.user.get_full_name(),
        'now': specific_date,
        'escudo_base64': escudo_base64,  # Incluir la imagen en base64 en el contexto
    }
    
    # Renderiza la plantilla HTML utilizando el contexto proporcionado, generando
    # una cadena de texto HTML.
    html = template.render(context)
    
    # Crea un buffer en memoria para almacenar los datos binarios del PDF.
    response = BytesIO()
    
    # Utiliza pisa para convertir el HTML en un documento PDF y lo almacena en el buffer response.
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
    
    # Verifica si hubo algún error durante la generación del PDF.
    if not pdf.err:
        # Devuelve una respuesta HTTP con el contenido del PDF, estableciendo el encabezado
        # 'Content-Disposition' para que el PDF se muestre en el navegador con el nombre de archivo especificado.
        return HttpResponse(response.getvalue(), content_type='application/pdf', headers={'Content-Disposition': f'inline; filename="{filename}"'})
    else:
        # Si hubo un error en la generación del PDF, devuelve una respuesta HTTP
        # con un mensaje de error y un estado HTTP 500 (Internal Server Error).
        return HttpResponse('Error al generar el PDF', status=500)


#------------------------------------esta funcion se encarga de subir el pdf al dopzonde despues de la firma digital-------------------------------------------------------------


from django.http import JsonResponse
import mimetypes
import os
from PyPDF2 import PdfReader

def verificar_firma_digital(pdf):
    try:
        # Abre el archivo PDF usando PyPDF2
        reader = PdfReader(pdf)
        
        # Revisa si el PDF tiene un campo de firma digital
        if '/AcroForm' in reader.trailer['/Root']:
            acroform = reader.trailer['/Root']['/AcroForm']
            if '/SigFlags' in acroform:
                return True
        return False
    except Exception as e:
        return False

def subir_pdf(request):
    if request.method == 'POST':
        if 'pdf' in request.FILES:
            pdf = request.FILES['pdf']
            mime_type, _ = mimetypes.guess_type(pdf.name)
            if mime_type != 'application/pdf':
                return JsonResponse({'error': 'El archivo seleccionado no es un PDF.'})

            # Verificar si tiene firma digital
            if not verificar_firma_digital(pdf):
                return JsonResponse({'error': 'El PDF no contiene una firma digital válida.'})

            try:
                folder = 'partespdf/'
                fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, folder))
                filename = fs.save(pdf.name, pdf)
                new_pdf = UploadedPDF(file=os.path.join(folder, filename), uploaded_by=request.user)
                new_pdf.save()
                return JsonResponse({'success': 'El archivo PDF se ha subido correctamente.'})
            except Exception as e:
                return JsonResponse({'error': f'Error al subir el archivo: {str(e)}'})
        else:
            return JsonResponse({'error': 'No se seleccionó ningún archivo.'})
    return render(request, 'comisarias/subir_pdf.html')


#-----------------------------------funcion para ver todos los registros  de los pdf--------------------------------------------------------------



from django.http import FileResponse

def ver_pdfs(request):
    # Obtiene todos los registros de PDF almacenados en la base de datos
    pdfs = UploadedPDF.objects.all()
    
    # Renderiza la plantilla 'ver_pdfs.html' y pasa los registros de PDF al contexto
    return render(request, 'comisarias/ver_pdfs.html', {'pdfs': pdfs})

def mostrar_pdf(request, pdf_id):
    # Obtiene el objeto UploadedPDF por ID
    pdf = UploadedPDF.objects.get(id=pdf_id)
    
    # Abre el archivo desde el sistema de archivos
    pdf_path = pdf.file.path
    response = FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')
    
    # Asegúrate de que el PDF se abra en el navegador en lugar de descargarse
    response['Content-Disposition'] = 'inline; filename="%s"' % pdf.file.name
    
    return response


#-----------------------aqui empieza las funciones de comisarias segunda----------------------------------------------------


# Repite las siguientes funciones para las demás comisarías...
def generate_comisaria_segunda_pdf_view(request):
    return view_pdf_content(request, ComisariaSegunda)

#------------------------------------------------------------------------------------------------------------------
def generate_comisaria_segunda_pdf_download(request):
    add_signature = 'signature' in request.GET
    now = datetime.now()

    # Obtiene el nombre de la comisaría desde el modelo (por ejemplo, "Comisaria Primera").
    comisaria_name = ComisariaSegunda._meta.verbose_name.title().replace(' ', '-')
    
    # Define el nombre del archivo, incluyendo "libro-diario", el nombre de la comisaría, y la fecha actual.
    filename = f"libro-diario-{comisaria_name}-Ush-{now.strftime('%d-%m-%Y')}.pdf"
    

    return generate_pdf(request, ComisariaSegunda, filename, add_signature=add_signature)

#------------------------------descargar de comisaria segunda pdf del dia anterior------------------------------------------------------

# Función para descargar el PDF del día anterior
def generate_comisaria_segunda_pdf_download_previous_day(request):
    # Verifica si la URL contiene el parámetro 'signature' en la cadena de consulta (GET).
    add_signature = 'signature' in request.GET
    
    # Obtiene la fecha y hora actual.
    now = datetime.now()

    # Obtiene el nombre de la comisaría desde el modelo (por ejemplo, "Comisaria Primera").
    comisaria_name = ComisariaSegunda._meta.verbose_name.title().replace(' ', '-')
    
    # Calcula la fecha del día anterior.
    previous_day = now - timedelta(days=1)
    
    # Define el nombre del archivo para el PDF, incluyendo "parte-diario", 
    # la fecha del día anterior, y la extensión ".pdf".
    filename = f"libro-diario-{comisaria_name}-Ush-{previous_day.strftime('%d-%m-%Y')}.pdf"
    
    # Llama a la función generate_pdf_for_specific_date, pasando el request, 
    # el modelo ComisariaPrimera, la fecha del día anterior, el nombre del archivo,
    # y el valor de add_signature. Esta función generará el PDF para la fecha específica
    # y lo devolverá como una respuesta HTTP.
    return generate_pdf_for_specific_date(request, ComisariaSegunda, previous_day, filename, add_signature=add_signature)


#--------------------------aqui empieza comisiaria tercefra los pdf------------------------------------------------------


def generate_comisaria_tercera_pdf_view(request):
    return view_pdf_content(request, ComisariaTercera)

#------------------------------------------------------------------------------------------------------------------
def generate_comisaria_tercera_pdf_download(request):
    add_signature = 'signature' in request.GET
    now = datetime.now()

    # Obtiene el nombre de la comisaría desde el modelo (por ejemplo, "Comisaria Tercera").
    comisaria_name = ComisariaTercera._meta.verbose_name.title().replace(' ', '-')
    
    # Define el nombre del archivo, incluyendo "libro-diario", el nombre de la comisaría, y la fecha actual.
    filename = f"libro-diario-{comisaria_name}-Ush-{now.strftime('%d-%m-%Y')}.pdf"

    return generate_pdf(request, ComisariaTercera, filename, add_signature=add_signature)

#------------------------------Descargar PDF del día anterior para Comisaria Tercera----------------------------------------

def generate_comisaria_tercera_pdf_download_previous_day(request):
    # Verifica si la URL contiene el parámetro 'signature' en la cadena de consulta (GET).
    add_signature = 'signature' in request.GET
    
    # Obtiene la fecha y hora actual.
    now = datetime.now()

    # Obtiene el nombre de la comisaría desde el modelo (por ejemplo, "Comisaria Tercera").
    comisaria_name = ComisariaTercera._meta.verbose_name.title().replace(' ', '-')
    
    # Calcula la fecha del día anterior.
    previous_day = now - timedelta(days=1)
    
    # Define el nombre del archivo para el PDF, incluyendo "libro-diario", 
    # la fecha del día anterior, y la extensión ".pdf".
    filename = f"libro-diario-{comisaria_name}-Ush-{previous_day.strftime('%d-%m-%Y')}.pdf"
    
    # Genera el PDF para la fecha específica y lo devuelve como una respuesta HTTP.
    return generate_pdf_for_specific_date(request, ComisariaTercera, previous_day, filename, add_signature=add_signature)



#-----------------------aqui empieza comisaria cuarta las funciones pdf ---------------------------------------------

def generate_comisaria_cuarta_pdf_view(request):
    return view_pdf_content(request, ComisariaCuarta)



#------------------------------------------------------------------------------------------------------------------
def generate_comisaria_cuarta_pdf_download(request):
    add_signature = 'signature' in request.GET
    now = datetime.now()

    # Obtiene el nombre de la comisaría desde el modelo (por ejemplo, "Comisaria Tercera").
    comisaria_name = ComisariaCuarta._meta.verbose_name.title().replace(' ', '-')
    
    # Define el nombre del archivo, incluyendo "libro-diario", el nombre de la comisaría, y la fecha actual.
    filename = f"libro-diario-{comisaria_name}-Ush-{now.strftime('%d-%m-%Y')}.pdf"

    return generate_pdf(request, ComisariaCuarta, filename, add_signature=add_signature)


#------------------------------Descargar PDF del día anterior para Comisaria Tercera----------------------------------------

def generate_comisaria_cuarta_pdf_download_previous_day(request):
    # Verifica si la URL contiene el parámetro 'signature' en la cadena de consulta (GET).
    add_signature = 'signature' in request.GET
    
    # Obtiene la fecha y hora actual.
    now = datetime.now()

    # Obtiene el nombre de la comisaría desde el modelo (por ejemplo, "Comisaria Tercera").
    comisaria_name = ComisariaCuarta._meta.verbose_name.title().replace(' ', '-')
    
    # Calcula la fecha del día anterior.
    previous_day = now - timedelta(days=1)
    
    # Define el nombre del archivo para el PDF, incluyendo "libro-diario", 
    # la fecha del día anterior, y la extensión ".pdf".
    filename = f"libro-diario-{comisaria_name}-Ush-{previous_day.strftime('%d-%m-%Y')}.pdf"
    
    # Genera el PDF para la fecha específica y lo devuelve como una respuesta HTTP.
    return generate_pdf_for_specific_date(request, ComisariaCuarta, previous_day, filename, add_signature=add_signature)



#-----------------------aqui empieza comisaria cuarta las funciones pdf ---------------------------------------------

def generate_comisaria_quinta_pdf_view(request):
    return view_pdf_content(request, ComisariaQuinta)



#------------------------------------------------------------------------------------------------------------------
def generate_comisaria_quinta_pdf_download(request):
    add_signature = 'signature' in request.GET
    now = datetime.now()

    # Obtiene el nombre de la comisaría desde el modelo (por ejemplo, "Comisaria Tercera").
    comisaria_name = ComisariaQuinta._meta.verbose_name.title().replace(' ', '-')
    
    # Define el nombre del archivo, incluyendo "libro-diario", el nombre de la comisaría, y la fecha actual.
    filename = f"libro-diario-{comisaria_name}-Ush-{now.strftime('%d-%m-%Y')}.pdf"

    return generate_pdf(request, ComisariaQuinta, filename, add_signature=add_signature)


#------------------------------Descargar PDF del día anterior para Comisaria Tercera----------------------------------------

def generate_comisaria_quinta_pdf_download_previous_day(request):
    # Verifica si la URL contiene el parámetro 'signature' en la cadena de consulta (GET).
    add_signature = 'signature' in request.GET
    
    # Obtiene la fecha y hora actual.
    now = datetime.now()

    # Obtiene el nombre de la comisaría desde el modelo (por ejemplo, "Comisaria Tercera").
    comisaria_name = ComisariaQuinta._meta.verbose_name.title().replace(' ', '-')
    
    # Calcula la fecha del día anterior.
    previous_day = now - timedelta(days=1)
    
    # Define el nombre del archivo para el PDF, incluyendo "libro-diario", 
    # la fecha del día anterior, y la extensión ".pdf".
    filename = f"libro-diario-{comisaria_name}-Ush-{previous_day.strftime('%d-%m-%Y')}.pdf"
    
    # Genera el PDF para la fecha específica y lo devuelve como una respuesta HTTP.
    return generate_pdf_for_specific_date(request, ComisariaQuinta, previous_day, filename, add_signature=add_signature)


#--------------------FUNCION PARA VER LOS PARTES------------------------------------------------

def serve_pdf(request, folder_name):
    # Define la ruta base
    base_path = os.path.join(settings.MEDIA_ROOT, folder_name)

    # Verifica si la carpeta existe
    if not os.path.exists(base_path):
        return render(request, '404.html', status=404)

    # Construye una lista de archivos con datos enriquecidos nuevos cambios
    files = []
    for file_name in os.listdir(base_path):
        file_path = os.path.join(base_path, file_name)
        if os.path.isfile(file_path):
            files.append({
                'name': file_name,
                'modified_at': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%d/%m/%Y %H:%M:%S'),
                'url': f"{settings.MEDIA_URL}{folder_name}/{file_name}",
            })

    # Renderiza la plantilla con los datos
    return render(request, 'comisarias/pdf_list.html', {'folder_name': folder_name, 'files': files})

#-----------FUNCION PARA GENERAR LA VISTA QUE MANEJA EL RANGO Y HORARIO SELECCIONADO----------#

def generate_pdf_for_date_and_range(request, comisaria_model, start_time, end_time, filename, comisaria_title, add_signature=False ):
    """
    Genera un PDF basado en un rango de fechas y horas especificado para una comisaría específica.
    """
    # Filtrar los registros en el rango horario
    registros = comisaria_model.objects.filter(
        models.Q(created_at__range=(start_time, end_time)) |
        models.Q(updated_at__range=(start_time, end_time)),
        activo=True  # Filtrar solo registros activos
    )

    # Cargar la plantilla HTML
    template = get_template('comisarias/comisarias_pdf_template.html')  # Ajustar ruta para la nueva app

    # Convertir la imagen a base64
    escudo_path = os.path.join(settings.BASE_DIR, 'comisarias', 'static', 'comisarias', 'images', 'ESCUDO POLICIA.jpeg')
    with open(escudo_path, "rb") as img_file:
        escudo_base64 = base64.b64encode(img_file.read()).decode('utf-8')

    # Preparar el contexto para la plantilla
    context = {
        'registros': registros,
        'comisaria_name': comisaria_title,
        'add_signature': add_signature,
        'username': request.user.get_full_name(),
        'start_time': start_time,
        'end_time': end_time,
        'escudo_base64': escudo_base64,
    }

    # Renderizar la plantilla HTML
    html = template.render(context)

    # Crear un buffer en memoria para el PDF
    response = BytesIO()

    # Generar el PDF a partir del HTML renderizado
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)

    # Verificar si la generación del PDF fue exitosa
    if not pdf.err:
        return HttpResponse(
            response.getvalue(),
            content_type='application/pdf',
            headers={'Content-Disposition': f'inline; filename="{filename}"'}
        )
    else:
        return HttpResponse('Error al generar el PDF', status=500)
    
#-----------FUNCION PARA GENERAR LA VISTA QUE MANEJA EL RANGO Y HORARIO SELECCIONADO----------#

def generate_pdf_custom_range_view_ush(request):
    # Obtener los valores del formulario
    start_date = request.GET.get('start_date')  # Formato: 'YYYY-MM-DD'
    start_time = request.GET.get('start_time')  # Formato: 'HH:MM'
    end_date = request.GET.get('end_date')      # Formato: 'YYYY-MM-DD'
    end_time = request.GET.get('end_time')      # Formato: 'HH:MM'
    comisaria_name = request.GET.get('comisaria')  # Nombre de la comisaría seleccionada

    # Mapear el nombre de la comisaría al modelo
    comisaria_map = {
        'primera': ComisariaPrimera,
        'segunda': ComisariaSegunda,
        'tercera': ComisariaTercera,
        'cuarta': ComisariaCuarta,
        'quinta': ComisariaQuinta,
    }
    
    # Mapear el modelo y el nombre de la comisaría 

    comisaria_title_map = {
    'primera': 'Comisaria Primera',
    'segunda': 'Comisaria Segunda',
    'tercera': 'Comisaria Tercera',
    'cuarta': 'Comisaria Cuarta',
    'quinta': 'Comisaria Quinta',
    }

    comisaria_model = comisaria_map.get(comisaria_name)
    comisaria_title = comisaria_title_map.get(comisaria_name)

    if not comisaria_title:
        return HttpResponse('Comisaría no válida', status=400)

    # Combinar fecha y hora en objetos datetime
    try:
        start_datetime = datetime.strptime(f"{start_date} {start_time}", '%Y-%m-%d %H:%M')
        end_datetime = datetime.strptime(f"{end_date} {end_time}", '%Y-%m-%d %H:%M')
    except (ValueError, TypeError):
        return HttpResponse('Error en el formato de fecha/hora', status=400)
 

    # Usar el nombre completo de la comisaría en el título del archivo
    filename = f"libro-diario-{comisaria_title.replace(' ', '_')}-{start_datetime.strftime('%Y-%m-%d_%H-%M')}_to_{end_datetime.strftime('%Y-%m-%d_%H-%M')}.pdf"
    return generate_pdf_for_date_and_range(request, comisaria_model, start_datetime, end_datetime, filename, comisaria_title=comisaria_title)
    
#----------FUNCION PARA RENDERIZAR LA VISTA----------
def select_range_view_ush(request):
    # Renderizar el formulario para seleccionar el rango
    return render(request, 'comisarias/select_range_ushuaia.html')