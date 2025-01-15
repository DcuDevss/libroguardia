import os
import json
import mimetypes
from datetime import datetime, timedelta
from io import BytesIO
import re

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
from .forms import ComisariaPrimeraRGForm, ComisariaSegundaRGForm, ComisariaTerceraRGForm, ComisariaCuartaRGForm, ComisariaQuintaRGForm, CustomLoginForm
from .models import ComisariaPrimeraRG, ComisariaSegundaRG, ComisariaTerceraRG, ComisariaCuartaRG, ComisariaQuintaRG, DependenciasSecundariasRG, CodigoPolicialRG, DetalleDependenciaSecundariaRG, DetalleInstitucionFederal, DetalleServicioEmergenciaRG, DetalleInstitucionHospitalariaRG, DetalleDependenciaMunicipalRG, DetalleDependenciaProvincialRG 
from compartido.models import UploadedPDFRG

from compartido.utils import user_is_in_group
import base64


#------------------funcion par de realizar las firmas--------------------------------------------

@login_required
def sign_comisaria_primeraRG(request, pk):
    # Obtiene la instancia de ComisariaPrimeraRG correspondiente al ID (pk) proporcionado.
    # Si no se encuentra, lanza una excepción 404.
    comisaria = get_object_or_404(ComisariaPrimeraRG, pk=pk)
    
    # Obtiene el nombre completo del usuario actual, o su nombre de usuario si el nombre completo no está disponible.
    user_full_name = request.user.get_full_name() or request.user.username
    
    # Verifica si ya hay firmas en la instancia de ComisariaPrimeraRG.
    if comisaria.firmas:
        # Si ya existen firmas, añade la firma del usuario actual, separada por una coma.
        comisaria.firmas += f", {user_full_name}"
    else:
        # Si no hay firmas previas, establece la firma del usuario actual como la primera firma.
        comisaria.firmas = user_full_name
    
    # Guarda los cambios en la instancia de ComisariaPrimeraRG, pero solo actualiza el campo 'firmas'.
    comisaria.save(update_fields=['firmas'])  # Solo actualiza el campo firmas
    
    # Redirige al usuario a la vista de la lista de ComisariaPrimeraRG después de firmar.
    return redirect(reverse('comisaria_primeraRG_list'))
#-------------------------------------------------------------------------------------------------------

# Función para firmar en Comisaria SegundaRG
@login_required
def sign_comisaria_segundaRG(request, pk):
    comisaria = get_object_or_404(ComisariaSegundaRG, pk=pk)
    user_full_name = request.user.get_full_name() or request.user.username
    if comisaria.firmas:
        comisaria.firmas += f", {user_full_name}"
    else:
        comisaria.firmas = user_full_name
    comisaria.save(update_fields=['firmas'])  # Solo actualiza el campo firmas
    return redirect(reverse('comisaria_segundaRG_list'))

#---------------------------------------------------------------------------------------------------------

# Función para firmar en Comisaria TerceraRG
@login_required
def sign_comisaria_terceraRG(request, pk):
    comisaria = get_object_or_404(ComisariaTerceraRG, pk=pk)
    user_full_name = request.user.get_full_name() or request.user.username
    if comisaria.firmas:
        comisaria.firmas += f", {user_full_name}"
    else:
        comisaria.firmas = user_full_name
    comisaria.save(update_fields=['firmas'])  # Solo actualiza el campo firmas
    return redirect(reverse('comisaria_terceraRG_list'))

#-------------------------------------------------------------------------------------------------

# Función para firmar en Comisaria CuartaRG
@login_required
def sign_comisaria_cuartaRG(request, pk):
    comisaria = get_object_or_404(ComisariaCuartaRG, pk=pk)
    user_full_name = request.user.get_full_name() or request.user.username
    if comisaria.firmas:
        comisaria.firmas += f", {user_full_name}"
    else:
        comisaria.firmas = user_full_name
    comisaria.save(update_fields=['firmas'])  # Solo actualiza el campo firmas
    return redirect(reverse('comisaria_cuartaRG_list'))

#--------------------------------------------------------------------------------------------

# Función para firmar en Comisaria QuintaRG
@login_required
def sign_comisaria_quintaRG(request, pk):
    comisaria = get_object_or_404(ComisariaQuintaRG, pk=pk)
    user_full_name = request.user.get_full_name() or request.user.username
    if comisaria.firmas:
        comisaria.firmas += f", {user_full_name}"
    else:
        comisaria.firmas = user_full_name
    comisaria.save(update_fields=['firmas'])  # Solo actualiza el campo firmas
    return redirect(reverse('comisaria_quintaRG_list'))

#-------------------clase para ver la tabla los codigos comisariaprimeraRG filtrando con los permisos-------------------------------------------------------------------------

# views.py

class ComisariaPrimeraRGListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    # Especifica el modelo de datos que se va a listar.
    model = ComisariaPrimeraRG
    
    # Define la plantilla que se utilizará para renderizar la lista.
    template_name = 'comisariasriogrande/primeraRG/comisaria_primeraRG_list.html'
    
    # Define el nombre del contexto que contendrá la lista de registros.
    context_object_name = 'records'

    # Método que determina si el usuario tiene permiso para acceder a esta vista.
    def test_func(self):
        # Verifica si el usuario pertenece al grupo 'comisariaprimeraRG'.
        return user_is_in_group(self.request.user, 'comisariaprimeraRG')

    # Método que maneja el caso en el que el usuario no tiene permiso para acceder a la vista.
    def handle_no_permission(self):
        # Redirige al usuario a la página de 'no_permission' si no tiene permiso.
        return redirect('no_permission')
    #funcion paginado----09/01/25
    def get_paginate_by(self, queryset):
        # Determina cuántos elementos se mostrarán por página, según un parámetro GET.

        items_per_page = self.request.GET.get('items_per_page', 10)  # Obtiene el valor de `items_per_page` (o 10 por defecto).
        try:
            return int(items_per_page)  # Intenta convertir el valor a entero.
        except ValueError:
            return 10  # Si ocurre un error, devuelve el valor por defecto (10).
    #cierre----09/01/25
    # Método que personaliza el conjunto de datos que se listará en la vista--09/01/25.
    def get_queryset(self):
        # Obtiene el queryset predeterminado y lo ordena por la fecha y hora en orden descendente.
        #queryset = super().get_queryset().order_by('-fecha_hora')
        queryset = super().get_queryset().filter(activo=True).order_by('-fecha_hora')
        # Obtiene el parámetro de búsqueda de la solicitud GET, si existe.
        search_query = self.request.GET.get('q', '')
        
        # Si hay una consulta de búsqueda, filtra el queryset por coincidencias en el campo 'cuarto'.
        if search_query:  # Verifica si se ingresó un término de búsqueda.
            try:
                search_date = datetime.strptime(search_query, "%d/%m/%Y").date()  
                # Intenta convertir la consulta a una fecha (sin hora) usando el formato 'dd/mm/yyyy'.
                queryset = queryset.filter(fecha_hora__date=search_date)  
                # Filtra los registros donde solo la fecha (sin hora) coincide.
            except (ValueError, TypeError):  
                # Si la consulta no es una fecha válida, realiza el filtrado en otros campos.
                queryset = queryset.filter(
                       Q(codigoRG__codigoRG__icontains=search_query) |
                        Q(codigoRG__nombre_codigo__icontains=search_query) |
                        Q(movil_patrulla__icontains=search_query) |
                        Q(a_cargo__icontains=search_query) |
                        Q(secundante__icontains=search_query) |
                        Q(lugar_codigo__icontains=search_query) |
                        Q(tareas_judiciales__icontains=search_query) |
                        Q(descripcion__icontains=search_query) |
                        Q(fecha_hora__icontains=search_query)
                    )
        
        # Devuelve el queryset final, posiblemente filtrado y ajustado.
        return queryset
    #cierre----09/01/25

    # Método que proporciona datos adicionales al contexto de la plantilla.
    def get_context_data(self, **kwargs):
        # Llama al método original para obtener el contexto predeterminado.
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Agrega informacion sobe permisos del usuario, segun ss grupos.
        context['is_jefessuperiores'] = user.groups.filter(name='jefessuperiores').exists()
        context['is_libreros'] = user.groups.filter(name='libreros').exists()
        context['is_encargadosguardias'] = user.groups.filter(name='encargadosguardias').exists()
        context['is_oficialesservicios'] = user.groups.filter(name='oficialesservicios').exists()
        context['is_comisariaprimeraRG'] = user.groups.filter(name='comisariaprimeraRG').exists()
        
        # Agrega la fecha actual al contexto.
        context['today'] = timezone.now().date()
        
        # Inicializa resolveId en None y lo agrega al contexto.
        context['resolveId'] = None  # Inicializa resolveId en None
    #paginado----09/01/25
        queryset = self.get_queryset()  # Obtiene el conjunto de datos filtrado.
        paginate_by = self.get_paginate_by(queryset)  # Determina el número de registros por página.
        paginator = Paginator(queryset, paginate_by)  # Crea el objeto de paginación con el conjunto de datos.
        page = self.request.GET.get('page')  # Obtiene el número de la página actual desde los parámetros GET.

        try:
            page_obj = paginator.page(page)  # Obtiene los registros correspondientes a la página actual.
        except PageNotAnInteger:
            page_obj = paginator.page(1)  # Si el número de página no es válido, muestra la primera página.
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)  # Si el número de página está fuera de rango, muestra la última página.

        current_page = page_obj.number  # Obtiene el número de la página actual.
        total_pages = page_obj.paginator.num_pages  # Calcula el número total de páginas.
        range_start = max(current_page - 5, 1)  # Calcula el inicio del rango dinámico de paginación.
        range_end = min(current_page + 5, total_pages) + 1  # Calcula el final del rango dinámico de paginación.

        context['page_obj'] = page_obj  # Añade el objeto de paginación al contexto.
        context['query'] = self.request.GET.get('q', '')  # Añade la consulta de búsqueda al contexto.
        context['items_per_page'] = paginate_by  # Añade el número de elementos por página al contexto.
        context['page_range'] = range(range_start, range_end)  # Añade el rango dinámico de páginas al contexto.

        #cierre----09/01/25
        # Devuelve el contexto completo.
        return context

#---------------------------clase para el create del formulario------------------------------------------------------------------------------------
   


class ComisariaPrimeraRGCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    # Especifica el modelo de datos que se va a crear.
    model = ComisariaPrimeraRG
    
    # Especifica el formulario que se utilizará para crear el objeto.
    form_class = ComisariaPrimeraRGForm
    
    # Define la plantilla que se utilizará para renderizar el formulario.
    template_name = 'comisariasriogrande/primeraRG/comisaria_primeraRG_form.html'
    
    # Define la URL a la que se redirigirá al usuario después de crear el objeto.
    success_url = reverse_lazy('comisaria_primeraRG_list')

    # Método que determina si el usuario tiene permiso para acceder a esta vista.
    def test_func(self):
        # Verifica si el usuario pertenece al grupo 'comisariaprimeraRG'.
        return user_is_in_group(self.request.user, 'comisariaprimeraRG')

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
        context['codigos_policialesRG'] = CodigoPolicialRG.objects.all()
        
        # Añade al contexto todos los objetos de DependenciasSecundariasRG.
        context['dependencias_secundariasRG'] = DependenciasSecundariasRG.objects.all()

        # Inicializa detalles adicionales como listas vacías en el contexto para la vista de creación.
        context['detalle_servicios_emergenciaRG'] = json.dumps([])
        context['detalle_instituciones_hospitalariasRG'] = json.dumps([])
        context['detalle_dependencias_municipalesRG'] = json.dumps([])
        context['detalle_dependencias_provincialesRG'] = json.dumps([])
        context['detalle_dependencias_secundariasRG'] = json.dumps([])
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
            for servicioRG in form.cleaned_data['servicios_emergenciaRG']:
                # Obtiene los datos específicos para cada servicio de emergencia desde el formulario.
                numero_movil_bomberosRG = self.request.POST.get(f'numero_movil_bomberos_{servicioRG.id}')
                nombre_a_cargo_bomberosRG = self.request.POST.get(f'nombre_a_cargo_bomberos_{servicioRG.id}')
                
                # Si se proporcionan datos, crea un registro en DetalleServicioEmergencia.
                if numero_movil_bomberosRG or nombre_a_cargo_bomberosRG:
                    DetalleServicioEmergenciaRG.objects.create(
                        servicio_emergenciaRG=servicioRG,
                        comisaria_primeraRG=self.object,
                        numero_movil_bomberosRG=numero_movil_bomberosRG,
                        nombre_a_cargo_bomberosRG=nombre_a_cargo_bomberosRG
                    )

            # Guardar los detalles adicionales para cada institución hospitalaria.
            for institucionRG in form.cleaned_data['instituciones_hospitalariasRG']:
                # Obtiene los datos específicos para cada institución hospitalaria desde el formulario.
                numero_movil_hospitalRG = self.request.POST.get(f'numero_movil_hospital_{institucionRG.id}')
                nombre_a_cargo_hospitalRG = self.request.POST.get(f'nombre_a_cargo_hospital_{institucionRG.id}')
                
                # Si se proporcionan datos, crea un registro en DetalleInstitucionHospitalaria.
                if numero_movil_hospitalRG or nombre_a_cargo_hospitalRG:
                    DetalleInstitucionHospitalariaRG.objects.create(
                        institucion_hospitalariaRG=institucionRG,
                        comisaria_primeraRG=self.object,
                        numero_movil_hospitalRG=numero_movil_hospitalRG,
                        nombre_a_cargo_hospitalRG=nombre_a_cargo_hospitalRG
                    )

            # Guardar los detalles adicionales para cada dependencia municipal.
            for dependencia_municipalRG in form.cleaned_data['dependencias_municipalesRG']:
                # Obtiene los datos específicos para cada dependencia municipal desde el formulario.
                numero_movil_municipalRG = self.request.POST.get(f'numero_movil_municipal_{dependencia_municipalRG.id}')
                nombre_a_cargo_municipalRG = self.request.POST.get(f'nombre_a_cargo_municipal_{dependencia_municipalRG.id}')
                
                # Si se proporcionan datos, crea un registro en DetalleDependenciaMunicipal.
                if numero_movil_municipalRG or nombre_a_cargo_municipalRG:
                    DetalleDependenciaMunicipalRG.objects.create(
                        dependencia_municipalRG=dependencia_municipalRG,
                        comisaria_primeraRG=self.object,
                        numero_movil_municipalRG=numero_movil_municipalRG,
                        nombre_a_cargo_municipalRG=nombre_a_cargo_municipalRG
                    )

            # Guardar los detalles adicionales para cada dependencia provincial.
            for dependencia_provincialRG in form.cleaned_data['dependencias_provincialesRG']:
                # Obtiene los datos específicos para cada dependencia provincial desde el formulario.
                numero_movil_provincialRG = self.request.POST.get(f'numero_movil_provincial_{dependencia_provincialRG.id}')
                nombre_a_cargo_provincialRG = self.request.POST.get(f'nombre_a_cargo_provincial_{dependencia_provincialRG.id}')
                
                # Si se proporcionan datos, crea un registro en DetalleDependenciaProvincial.
                if numero_movil_provincialRG or nombre_a_cargo_provincialRG:
                    DetalleDependenciaProvincialRG.objects.create(
                        dependencia_provincialRG=dependencia_provincialRG,
                        comisaria_primeraRG=self.object,
                        numero_movil_provincialRG=numero_movil_provincialRG,
                        nombre_a_cargo_provincialRG=nombre_a_cargo_provincialRG
                    )

            # Guardar los detalles adicionales para dependencias secundarias
            for dependencia_secundariaRG in form.cleaned_data['dependencias_secundariasRG']:
                numero_movil_secundariaRG = self.request.POST.get(f'numero_movil_secundaria_{dependencia_secundariaRG.id}')
                nombre_a_cargo_secundariaRG = self.request.POST.get(f'nombre_a_cargo_secundaria_{dependencia_secundariaRG.id}')
                if numero_movil_secundariaRG or nombre_a_cargo_secundariaRG:
                    DetalleDependenciaSecundariaRG.objects.create(
                        dependencia_secundariaRG=dependencia_secundariaRG,
                        comisaria_primeraRG=self.object,
                        numero_movil_secundariaRG=numero_movil_secundariaRG,
                        nombre_a_cargo_secundariaRG=nombre_a_cargo_secundariaRG
                    )

            # Guardar los detalles adicionales para instituciones federales
            for institucion_federal in form.cleaned_data['instituciones_federales']:
                numero_movil_federal = self.request.POST.get(f'numero_movil_federal_{institucion_federal.id}')
                nombre_a_cargo_federal = self.request.POST.get(f'nombre_a_cargo_federal_{institucion_federal.id}')
                if numero_movil_federal or nombre_a_cargo_federal:
                    DetalleInstitucionFederal.objects.create(
                        institucion_federal=institucion_federal,
                        comisaria_primeraRG=self.object,
                        numero_movil_federal=numero_movil_federal,
                        nombre_a_cargo_federal=nombre_a_cargo_federal
                    )        

            # Llama al método form_valid de la clase base para completar la operación.
            # Añadir un mensaje de éxito al sistema de mensajes
            messages.success(self.request, 'El código ha sido guardado exitosamente.')
            
            return super().form_valid(form)
        
 #------------------------clase para el edit updtae------------------------------------------------------


class ComisariaPrimeraRGUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # Especifica el modelo de datos que se va a actualizar.
    model = ComisariaPrimeraRG
    
    # Especifica el formulario que se utilizará para actualizar el objeto.
    form_class = ComisariaPrimeraRGForm
    
    # Define la plantilla que se utilizará para renderizar el formulario.
    template_name = 'comisariasriogrande/primeraRG/comisaria_primeraRG_form.html'
    
    # Define la URL a la que se redirigirá al usuario después de actualizar el objeto.
    success_url = reverse_lazy('comisaria_primeraRG_list')

    # Método que determina si el usuario tiene permiso para acceder a esta vista.
    def test_func(self):
        # Verifica si el usuario pertenece al grupo 'comisariaprimeraRG'.
        return user_is_in_group(self.request.user, 'comisariaprimeraRG')

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
            return redirect('comisaria_primeraRG_list')

        # Si no se cumplen las condiciones anteriores, sigue con el proceso normal.
        return super().dispatch(request, *args, **kwargs)

    # Método que proporciona datos adicionales al contexto de la plantilla.
    def get_context_data(self, **kwargs):
        # Llama al método original para obtener el contexto predeterminado.
        context = super().get_context_data(**kwargs)
        
        # Añade al contexto todos los objetos de CodigoPolicialUSH.
        context['codigos_policialesRG'] = CodigoPolicialRG.objects.all()
        
        # Añade al contexto todos los objetos de DependenciasSecundarias.
        context['dependencias_secundariasRG'] = DependenciasSecundariasRG.objects.all()

        # Convierte los detalles en JSON para ser usados por Alpine.js
        context['detalle_servicios_emergenciaRG'] = json.dumps(list(
            DetalleServicioEmergenciaRG.objects.filter(comisaria_primeraRG=self.object.pk).values('id', 'servicio_emergenciaRG_id', 'numero_movil_bomberosRG', 'nombre_a_cargo_bomberosRG')
        ))

        context['detalle_instituciones_hospitalariasRG'] = json.dumps(list(
            DetalleInstitucionHospitalariaRG.objects.filter(comisaria_primeraRG=self.object.pk).values('id', 'institucion_hospitalariaRG_id', 'numero_movil_hospitalRG', 'nombre_a_cargo_hospitalRG')
        ))

        context['detalle_dependencias_municipalesRG'] = json.dumps(list(
            DetalleDependenciaMunicipalRG.objects.filter(comisaria_primeraRG=self.object.pk).values('id', 'dependencia_municipalRG_id', 'numero_movil_municipalRG', 'nombre_a_cargo_municipalRG')
        ))

        context['detalle_dependencias_provincialesRG'] = json.dumps(list(
            DetalleDependenciaProvincialRG.objects.filter(comisaria_primeraRG=self.object.pk).values('id', 'dependencia_provincialRG_id', 'numero_movil_provincialRG', 'nombre_a_cargo_provincialRG')
        ))

         # Añadir los nuevos detalles para dependencias secundarias
        context['detalle_dependencias_secundariasRG'] = json.dumps(list(
            DetalleDependenciaSecundariaRG.objects.filter(comisaria_primeraRG=self.object.pk).values('id', 'dependencia_secundariaRG_id', 'numero_movil_secundariaRG', 'nombre_a_cargo_secundariaRG')
        ))

        # Añadir los nuevos detalles para instituciones federales
        context['detalle_instituciones_federales'] = json.dumps(list(
            DetalleInstitucionFederal.objects.filter(comisaria_primeraRG=self.object.pk).values('id', 'institucion_federal_id', 'numero_movil_federal', 'nombre_a_cargo_federal')
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
        servicios_emergencia_ids = form.cleaned_data['servicios_emergenciaRG'].values_list('id', flat=True)
        instituciones_hospitalarias_ids = form.cleaned_data['instituciones_hospitalariasRG'].values_list('id', flat=True)
        dependencias_municipales_ids = form.cleaned_data['dependencias_municipalesRG'].values_list('id', flat=True)
        dependencias_provinciales_ids = form.cleaned_data['dependencias_provincialesRG'].values_list('id', flat=True)
        dependencias_secundarias_ids = form.cleaned_data['dependencias_secundariasRG'].values_list('id', flat=True)
        instituciones_federales_ids = form.cleaned_data['instituciones_federales'].values_list('id', flat=True)


        # Eliminar los detalles que ya no están seleccionados.
        DetalleServicioEmergenciaRG.objects.filter(comisaria_primeraRG=self.object).exclude(servicio_emergenciaRG_id__in=servicios_emergencia_ids).delete()
        DetalleInstitucionHospitalariaRG.objects.filter(comisaria_primeraRG=self.object).exclude(institucion_hospitalariaRG_id__in=instituciones_hospitalarias_ids).delete()
        DetalleDependenciaMunicipalRG.objects.filter(comisaria_primeraRG=self.object).exclude(dependencia_municipalRG_id__in=dependencias_municipales_ids).delete()
        DetalleDependenciaProvincialRG.objects.filter(comisaria_primeraRG=self.object).exclude(dependencia_provincialRG_id__in=dependencias_provinciales_ids).delete()
        DetalleDependenciaSecundariaRG.objects.filter(comisaria_primeraRG=self.object).exclude(dependencia_secundariaRG_id__in=dependencias_secundarias_ids).delete()
        DetalleInstitucionFederal.objects.filter(comisaria_primeraRG=self.object).exclude(institucion_federal_id__in=instituciones_federales_ids).delete()


        # Guardar los detalles adicionales para cada servicio de emergencia.
        for servicioRG in form.cleaned_data['servicios_emergenciaRG']:
            numero_movil_bomberosRG = self.request.POST.get(f'numero_movil_bomberos_{servicioRG.id}')
            nombre_a_cargo_bomberosRG = self.request.POST.get(f'nombre_a_cargo_bomberos_{servicioRG.id}')
            DetalleServicioEmergenciaRG.objects.update_or_create(
                servicio_emergenciaRG=servicioRG,
                comisaria_primeraRG=self.object,
                defaults={
                    'numero_movil_bomberosRG': numero_movil_bomberosRG,
                    'nombre_a_cargo_bomberosRG': nombre_a_cargo_bomberosRG
                }
            )

        # Guardar los detalles adicionales para cada institución hospitalaria.
        for institucionRG in form.cleaned_data['instituciones_hospitalariasRG']:
            numero_movil_hospitalRG = self.request.POST.get(f'numero_movil_hospital_{institucionRG.id}')
            nombre_a_cargo_hospitalRG= self.request.POST.get(f'nombre_a_cargo_hospital_{institucionRG.id}')
            DetalleInstitucionHospitalariaRG.objects.update_or_create(
                institucion_hospitalariaRG=institucionRG,
                comisaria_primeraRG=self.object,
                defaults={
                    'numero_movil_hospitalRG': numero_movil_hospitalRG,
                    'nombre_a_cargo_hospitalRG': nombre_a_cargo_hospitalRG
                }
            )

        # Guardar los detalles adicionales para cada dependencia municipal.
        for dependencia_municipalRG in form.cleaned_data['dependencias_municipalesRG']:
            numero_movil_municipalRG = self.request.POST.get(f'numero_movil_municipal_{dependencia_municipalRG.id}')
            nombre_a_cargo_municipalRG = self.request.POST.get(f'nombre_a_cargo_municipal_{dependencia_municipalRG.id}')
            DetalleDependenciaMunicipalRG.objects.update_or_create(
                dependencia_municipalRG=dependencia_municipalRG,
                comisaria_primeraRG=self.object,
                defaults={
                    'numero_movil_municipalRG': numero_movil_municipalRG,
                    'nombre_a_cargo_municipalRG': nombre_a_cargo_municipalRG
                }
            )

        # Guardar los detalles adicionales para cada dependencia provincial.
        for dependencia_provincialRG in form.cleaned_data['dependencias_provincialesRG']:
            numero_movil_provincialRG = self.request.POST.get(f'numero_movil_provincial_{dependencia_provincialRG.id}')
            nombre_a_cargo_provincialRG = self.request.POST.get(f'nombre_a_cargo_provincial_{dependencia_provincialRG.id}')
            DetalleDependenciaProvincialRG.objects.update_or_create(
                dependencia_provincialRG=dependencia_provincialRG,
                comisaria_primeraRG=self.object,
                defaults={
                    'numero_movil_provincialRG': numero_movil_provincialRG,
                    'nombre_a_cargo_provincialRG': nombre_a_cargo_provincialRG
                }
            )

          # Guardar detalles adicionales para cada dependencia secundaria
        for dependencia_secundariaRG in form.cleaned_data['dependencias_secundariasRG']:
            numero_movil_secundariaRG = self.request.POST.get(f'numero_movil_secundaria_{dependencia_secundariaRG.id}')
            nombre_a_cargo_secundariaRG = self.request.POST.get(f'nombre_a_cargo_secundaria_{dependencia_secundariaRG.id}')
            DetalleDependenciaSecundariaRG.objects.update_or_create(
                dependencia_secundariaRG=dependencia_secundariaRG,
                comisaria_primeraRG=self.object,
                defaults={
                    'numero_movil_secundariaRG': numero_movil_secundariaRG,
                    'nombre_a_cargo_secundariaRG': nombre_a_cargo_secundariaRG
                }
            )

        # Guardar detalles adicionales para instituciones federales
        for institucion_federal in form.cleaned_data['instituciones_federales']:
            numero_movil_federal = self.request.POST.get(f'numero_movil_federal_{institucion_federal.id}')
            nombre_a_cargo_federal = self.request.POST.get(f'nombre_a_cargo_federal_{institucion_federal.id}')
            DetalleInstitucionFederal.objects.update_or_create(
                institucion_federal=institucion_federal,
                comisaria_primeraRG=self.object,
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



class ComisariaPrimeraRGDetailView(DetailView):
    model = ComisariaPrimeraRG
    template_name = 'comisariasriogrande/primeraRG/comisaria_primeraRG_detail.html'
    context_object_name = 'record'




#----------------------------softdelete-------------------------------------------------------------

# En views.py

def eliminar_comisaria_primeraRG(request, pk):
    # Obtén el registro a eliminar
    comisaria = get_object_or_404(ComisariaPrimeraRG, pk=pk)
    
    # Marca el registro como inactivo
    comisaria.activo = False
    comisaria.save()
    
    # Envía un mensaje de confirmación
    messages.success(request, 'El código ha sido eliminado correctamente.')
    
    # Redirige de vuelta a la lista
    return redirect('comisaria_primeraRG_list')




#---------------------------------------------------------------------------------------------------------------------------------------


# Vistas de listado y creación para ComisariaSegundaRG, ComisariaTerceraRG, ComisariaCuartaRG, y ComisariaQuintaRG


class ComisariaSegundaRGListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ComisariaSegundaRG
    template_name = 'comisariasriogrande/segundaRG/comisaria_segundaRG_list.html'
    context_object_name = 'records'

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariasegundaRG')

    def handle_no_permission(self):
        return redirect('no_permission')
    #funcion paginado----09/01/25
    def get_paginate_by(self, queryset):
        # Determina cuántos elementos se mostrarán por página, según un parámetro GET.

        items_per_page = self.request.GET.get('items_per_page', 10)  # Obtiene el valor de `items_per_page` (o 10 por defecto).
        try:
            return int(items_per_page)  # Intenta convertir el valor a entero.
        except ValueError:
            return 10  # Si ocurre un error, devuelve el valor por defecto (10).
    #cierre----09/01/25
    def get_queryset(self):
        #queryset = super().get_queryset().order_by('-fecha_hora')
        queryset = super().get_queryset().filter(activo=True).order_by('-fecha_hora')
        search_query = self.request.GET.get('q', '')
       # Si hay una consulta de búsqueda, filtra el queryset por coincidencias en el campo 'cuarto'----09/01/25.
        if search_query:  # Verifica si se ingresó un término de búsqueda.
            try:
                search_date = datetime.strptime(search_query, "%d/%m/%Y").date()  
                # Intenta convertir la consulta a una fecha (sin hora) usando el formato 'dd/mm/yyyy'.
                queryset = queryset.filter(fecha_hora__date=search_date)  
                # Filtra los registros donde solo la fecha (sin hora) coincide.
            except (ValueError, TypeError):  
                # Si la consulta no es una fecha válida, realiza el filtrado en otros campos.
                queryset = queryset.filter(
                        Q(codigoRG__codigoRG__icontains=search_query) |
                        Q(codigoRG__nombre_codigo__icontains=search_query) |
                        Q(movil_patrulla__icontains=search_query) |
                        Q(a_cargo__icontains=search_query) |
                        Q(secundante__icontains=search_query) |
                        Q(lugar_codigo__icontains=search_query) |
                        Q(tareas_judiciales__icontains=search_query) |
                        Q(descripcion__icontains=search_query) |
                        Q(fecha_hora__icontains=search_query)
                    )

        return queryset
    #cierre----09/01/25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        #context['is_jefessuperiores'] = self.request.user.groups.filter(name='jefessuperiores').exists()
        #context['is_encargados_guardias_segundaRG'] = user.groups.filter(name='encargados_guardias_segundaRG').exists()
        context['is_jefessuperiores'] = user.groups.filter(name='jefessuperiores').exists()
        context['is_libreros'] = user.groups.filter(name='libreros').exists()
        context['is_encargadosguardias'] = user.groups.filter(name='encargadosguardias').exists()
        context['is_oficialesservicios'] = user.groups.filter(name='oficialesservicios').exists()
        context['is_comisariasegundaRG'] = user.groups.filter(name='comisariasegundaRG').exists()


        context['today'] = timezone.now().date()
        context['resolveId'] = None
    #--paginado----09/01/25
        queryset = self.get_queryset()  # Obtiene el conjunto de datos filtrado.
        paginate_by = self.get_paginate_by(queryset)  # Determina el número de registros por página.
        paginator = Paginator(queryset, paginate_by)  # Crea el objeto de paginación con el conjunto de datos.
        page = self.request.GET.get('page')  # Obtiene el número de la página actual desde los parámetros GET.

        try:
            page_obj = paginator.page(page)  # Obtiene los registros correspondientes a la página actual.
        except PageNotAnInteger:
            page_obj = paginator.page(1)  # Si el número de página no es válido, muestra la primera página.
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)  # Si el número de página está fuera de rango, muestra la última página.

        current_page = page_obj.number  # Obtiene el número de la página actual.
        total_pages = page_obj.paginator.num_pages  # Calcula el número total de páginas.
        range_start = max(current_page - 5, 1)  # Calcula el inicio del rango dinámico de paginación.
        range_end = min(current_page + 5, total_pages) + 1  # Calcula el final del rango dinámico de paginación.

        context['page_obj'] = page_obj  # Añade el objeto de paginación al contexto.
        context['query'] = self.request.GET.get('q', '')  # Añade la consulta de búsqueda al contexto.
        context['items_per_page'] = paginate_by  # Añade el número de elementos por página al contexto.
        context['page_range'] = range(range_start, range_end)  # Añade el rango dinámico de páginas al contexto.

        return context
    #cierre----09/01/25

#-----------------------------------------------------------------------------------------------------------------   
    

class ComisariaSegundaRGCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ComisariaSegundaRG
    form_class = ComisariaSegundaRGForm
    template_name = 'comisariasriogrande/segundaRG/comisaria_segundaRG_form.html'
    success_url = reverse_lazy('comisaria_segundaRG_list')

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariasegundaRG')

    def handle_no_permission(self):
        return redirect('no_permission')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['codigos_policialesRG'] = CodigoPolicialRG.objects.all()
        context['dependencias_secundariasRG'] = DependenciasSecundariasRG.objects.all()

        # Inicializar detalles como listas vacías en el contexto
        context['detalle_servicios_emergenciaRG'] = json.dumps([])  # Para vista de creación, siempre es una lista vacía
        context['detalle_instituciones_hospitalariasRG'] = json.dumps([])
        context['detalle_dependencias_municipalesRG'] = json.dumps([])
        context['detalle_dependencias_provincialesRG'] = json.dumps([])
        context['detalle_dependencias_secundariasRG'] = json.dumps([])
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
        for servicioRG in form.cleaned_data['servicios_emergenciaRG']:
            numero_movil_bomberosRG = self.request.POST.get(f'numero_movil_bomberos_{servicioRG.id}')
            nombre_a_cargo_bomberosRG= self.request.POST.get(f'nombre_a_cargo_bomberos_{servicioRG.id}')
            if numero_movil_bomberosRG or nombre_a_cargo_bomberosRG:
                DetalleServicioEmergenciaRG.objects.create(
                    servicio_emergenciaRG=servicioRG,
                    comisaria_segundaRG=self.object,
                    numero_movil_bomberosRG=numero_movil_bomberosRG,
                    nombre_a_cargo_bomberosRG=nombre_a_cargo_bomberosRG
                )

        # Guardar los detalles adicionales para cada institución hospitalaria
        for institucionRG in form.cleaned_data['instituciones_hospitalariasRG']:
            numero_movil_hospitalRG = self.request.POST.get(f'numero_movil_hospital_{institucionRG.id}')
            nombre_a_cargo_hospitalRG = self.request.POST.get(f'nombre_a_cargo_hospital_{institucionRG.id}')
            if numero_movil_hospitalRG or nombre_a_cargo_hospitalRG:
                DetalleInstitucionHospitalariaRG.objects.create(
                    institucion_hospitalariaRG=institucionRG,
                    comisaria_segundaRG=self.object,
                    numero_movil_hospitalRG=numero_movil_hospitalRG,
                    nombre_a_cargo_hospitalRG=nombre_a_cargo_hospitalRG
                )

        # Guardar los detalles adicionales para cada dependencia municipal
        for dependencia_municipalRG in form.cleaned_data['dependencias_municipalesRG']:
            numero_movil_municipalRG = self.request.POST.get(f'numero_movil_municipal_{dependencia_municipalRG.id}')
            nombre_a_cargo_municipalRG = self.request.POST.get(f'nombre_a_cargo_municipal_{dependencia_municipalRG.id}')
            if numero_movil_municipalRG or nombre_a_cargo_municipalRG:
                DetalleDependenciaMunicipalRG.objects.create(
                    dependencia_municipalRG=dependencia_municipalRG,
                    comisaria_segundaRG=self.object,
                    numero_movil_municipalRG=numero_movil_municipalRG,
                    nombre_a_cargo_municipalRG=nombre_a_cargo_municipalRG
                )

        # Guardar los detalles adicionales para cada dependencia provincial
        for dependencia_provincialRG in form.cleaned_data['dependencias_provincialesRG']:
            numero_movil_provincialRG = self.request.POST.get(f'numero_movil_provincial_{dependencia_provincialRG.id}')
            nombre_a_cargo_provincialRG = self.request.POST.get(f'nombre_a_cargo_provincial_{dependencia_provincialRG.id}')
            if numero_movil_provincialRG or nombre_a_cargo_provincialRG:
                DetalleDependenciaProvincialRG.objects.create(
                    dependencia_provincialRG=dependencia_provincialRG,
                    comisaria_segundaRG=self.object,
                    numero_movil_provincialRG=numero_movil_provincialRG,
                    nombre_a_cargo_provincialRG=nombre_a_cargo_provincialRG
                )

         # Guardar los detalles adicionales para dependencias secundarias
        for dependencia_secundariaRG in form.cleaned_data['dependencias_secundariasRG']:
            numero_movil_secundariaRG = self.request.POST.get(f'numero_movil_secundaria_{dependencia_secundariaRG.id}')
            nombre_a_cargo_secundariaRG = self.request.POST.get(f'nombre_a_cargo_secundaria_{dependencia_secundariaRG.id}')
            if numero_movil_secundariaRG or nombre_a_cargo_secundariaRG:
                DetalleDependenciaSecundariaRG.objects.create(
                    dependencia_secundariaRG=dependencia_secundariaRG,
                    comisaria_segundaRG=self.object,
                    numero_movil_secundariaRG=numero_movil_secundariaRG,
                    nombre_a_cargo_secundariaRG=nombre_a_cargo_secundariaRG
                )

        # Guardar los detalles adicionales para instituciones federales
        for institucion_federal in form.cleaned_data['instituciones_federales']:
            numero_movil_federal = self.request.POST.get(f'numero_movil_federal_{institucion_federal.id}')
            nombre_a_cargo_federal = self.request.POST.get(f'nombre_a_cargo_federal_{institucion_federal.id}')
            if numero_movil_federal or nombre_a_cargo_federal:
                DetalleInstitucionFederal.objects.create(
                    institucion_federal=institucion_federal,
                    comisaria_segundaRG=self.object,
                    numero_movil_federal=numero_movil_federal,
                    nombre_a_cargo_federal=nombre_a_cargo_federal
                )         


        messages.success(self.request, 'El código ha sido guardado exitosamente.')
        return super().form_valid(form)


#--------------------------------------------------------------------------------------------------

class ComisariaSegundaRGUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ComisariaSegundaRG
    form_class = ComisariaSegundaRGForm
    template_name = 'comisariasriogrande/segundaRG/comisaria_segundaRG_form.html'
    success_url = reverse_lazy('comisaria_segundaRG_list')

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariasegundaRG')

    def handle_no_permission(self):
        return redirect('no_permission')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        now = timezone.now()

        if obj.fecha_hora.date() != now.date() and not obj.estado:
            return redirect('comisaria_segundaRG_list')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['codigos_policialesRG'] = CodigoPolicialRG.objects.all()
        context['dependencias_secundariasRG'] = DependenciasSecundariasRG.objects.all()

        # Convertir detalles en JSON para ser usados por Alpine.js
        context['detalle_servicios_emergenciaRG'] = json.dumps(list(
            DetalleServicioEmergenciaRG.objects.filter(comisaria_segundaRG=self.object.pk).values('id', 'servicio_emergenciaRG_id', 'numero_movil_bomberosRG', 'nombre_a_cargo_bomberosRG')
        ))

        context['detalle_instituciones_hospitalariasRG'] = json.dumps(list(
            DetalleInstitucionHospitalariaRG.objects.filter(comisaria_segundaRG=self.object.pk).values('id', 'institucion_hospitalariaRG_id', 'numero_movil_hospitalRG', 'nombre_a_cargo_hospitalRG')
        ))

        context['detalle_dependencias_municipalesRG'] = json.dumps(list(
            DetalleDependenciaMunicipalRG.objects.filter(comisaria_segundaRG=self.object.pk).values('id', 'dependencia_municipalRG_id', 'numero_movil_municipalRG', 'nombre_a_cargo_municipalRG')
        ))

        context['detalle_dependencias_provincialesRG'] = json.dumps(list(
            DetalleDependenciaProvincialRG.objects.filter(comisaria_segundaRG=self.object.pk).values('id', 'dependencia_provincialRG_id', 'numero_movil_provincialRG', 'nombre_a_cargo_provincialRG')
        ))

        # Añadir los nuevos detalles para dependencias secundarias
        context['detalle_dependencias_secundariasRG'] = json.dumps(list(
            DetalleDependenciaSecundariaRG.objects.filter(comisaria_segundaRG=self.object.pk).values('id', 'dependencia_secundariaRG_id', 'numero_movil_secundariaRG', 'nombre_a_cargo_secundariaRG')
        ))

        # Añadir los nuevos detalles para instituciones federales
        context['detalle_instituciones_federales'] = json.dumps(list(
            DetalleInstitucionFederal.objects.filter(comisaria_segundaRG=self.object.pk).values('id', 'institucion_federal_id', 'numero_movil_federal', 'nombre_a_cargo_federal')
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
        servicios_emergencia_ids = form.cleaned_data['servicios_emergenciaRG'].values_list('id', flat=True)
        instituciones_hospitalarias_ids = form.cleaned_data['instituciones_hospitalariasRG'].values_list('id', flat=True)
        dependencias_municipales_ids = form.cleaned_data['dependencias_municipalesRG'].values_list('id', flat=True)
        dependencias_provinciales_ids = form.cleaned_data['dependencias_provincialesRG'].values_list('id', flat=True)
        dependencias_secundarias_ids = form.cleaned_data['dependencias_secundariasRG'].values_list('id', flat=True)
        instituciones_federales_ids = form.cleaned_data['instituciones_federales'].values_list('id', flat=True)



        # Eliminar los detalles que ya no se arreglo están seleccionados
        DetalleServicioEmergenciaRG.objects.filter(comisaria_segundaRG=self.object).exclude(servicio_emergenciaRG_id__in=servicios_emergencia_ids).delete()
        DetalleInstitucionHospitalariaRG.objects.filter(comisaria_segundaRG=self.object).exclude(institucion_hospitalariaRG_id__in=instituciones_hospitalarias_ids).delete()
        DetalleDependenciaMunicipalRG.objects.filter(comisaria_segundaRG=self.object).exclude(dependencia_municipalRG_id__in=dependencias_municipales_ids).delete()
        DetalleDependenciaProvincialRG.objects.filter(comisaria_segundaRG=self.object).exclude(dependencia_provincialRG_id__in=dependencias_provinciales_ids).delete()
        DetalleDependenciaSecundariaRG.objects.filter(comisaria_segundaRG=self.object).exclude(dependencia_secundariaRG_id__in=dependencias_secundarias_ids).delete()
        DetalleInstitucionFederal.objects.filter(comisaria_segundaRG=self.object).exclude(institucion_federal_id__in=instituciones_federales_ids).delete()


        # Guardar los detalles adicionales para cada servicio de emergencia.
        for servicioRG in form.cleaned_data['servicios_emergenciaRG']:
            # Obtiene el número de móvil del formulario correspondiente a cada servicio de emergencia.
            numero_movil_bomberosRG = self.request.POST.get(f'numero_movil_bomberos_{servicioRG.id}')
    
            # Obtiene el nombre de la persona a cargo del formulario correspondiente a cada servicio de emergencia.
            nombre_a_cargo_bomberosRG = self.request.POST.get(f'nombre_a_cargo_bomberos_{servicioRG.id}')
    
            # Crea o actualiza un registro en la tabla DetalleServicioEmergencia.
            DetalleServicioEmergenciaRG.objects.update_or_create(

                 # Relaciona el registro con el servicio de emergencia actual.
                 servicio_emergenciaRG=servicioRG,
        
                 # Relaciona el registro con la instancia de ComisariaSegunda que se está editando o creando.
                 comisaria_segundaRG=self.object,
        
                 # Define los valores predeterminados para los campos que se van a actualizar o crear.
                 defaults={
                    'numero_movil_bomberosRG': numero_movil_bomberosRG,  # Asigna el número de móvil obtenido del formulario.
                    'nombre_a_cargo_bomberosRG': nombre_a_cargo_bomberosRG  # Asigna el nombre de la persona a cargo obtenido del formulario.
                }
            )
    

        # Guardar los detalles adicionales para cada institución hospitalaria
        for institucionRG in form.cleaned_data['instituciones_hospitalariasRG']:
            numero_movil_hospitalRG = self.request.POST.get(f'numero_movil_hospital_{institucionRG.id}')
            nombre_a_cargo_hospitalRG = self.request.POST.get(f'nombre_a_cargo_hospital_{institucionRG.id}')
            DetalleInstitucionHospitalariaRG.objects.update_or_create(
                institucion_hospitalariaRG=institucionRG,
                comisaria_segundaRG=self.object,
                defaults={
                    'numero_movil_hospitalRG': numero_movil_hospitalRG,
                    'nombre_a_cargo_hospitalRG': nombre_a_cargo_hospitalRG
                }
            )

        # Guardar los detalles adicionales para cada dependencia municipal
        for dependencia_municipalRG in form.cleaned_data['dependencias_municipalesRG']:
            numero_movil_municipalRG = self.request.POST.get(f'numero_movil_municipal_{dependencia_municipalRG.id}')
            nombre_a_cargo_municipalRG = self.request.POST.get(f'nombre_a_cargo_municipal_{dependencia_municipalRG.id}')
            DetalleDependenciaMunicipalRG.objects.update_or_create(
                dependencia_municipalRG=dependencia_municipalRG,
                comisaria_segundaRG=self.object,
                defaults={
                    'numero_movil_municipalRG': numero_movil_municipalRG,
                    'nombre_a_cargo_municipalRG': nombre_a_cargo_municipalRG
                }
            )

        # Guardar los detalles adicionales para cada dependencia provincial
        for dependencia_provincialRG in form.cleaned_data['dependencias_provincialesRG']:
            numero_movil_provincialRG = self.request.POST.get(f'numero_movil_provincial_{dependencia_provincialRG.id}')
            nombre_a_cargo_provincialRG = self.request.POST.get(f'nombre_a_cargo_provincial_{dependencia_provincialRG.id}')
            DetalleDependenciaProvincialRG.objects.update_or_create(
                dependencia_provincialRG=dependencia_provincialRG,
                comisaria_segundaRG=self.object,
                defaults={
                    'numero_movil_provincialRG': numero_movil_provincialRG,
                    'nombre_a_cargo_provincialRG': nombre_a_cargo_provincialRG
                }
            )

          # Guardar detalles adicionales para cada dependencia secundaria
        for dependencia_secundariaRG in form.cleaned_data['dependencias_secundariasRG']:
            numero_movil_secundariaRG = self.request.POST.get(f'numero_movil_secundaria_{dependencia_secundariaRG.id}')
            nombre_a_cargo_secundariaRG = self.request.POST.get(f'nombre_a_cargo_secundaria_{dependencia_secundariaRG.id}')
            DetalleDependenciaSecundariaRG.objects.update_or_create(
                dependencia_secundariaRG=dependencia_secundariaRG,
                comisaria_segundaRG=self.object,
                defaults={
                    'numero_movil_secundariaRG': numero_movil_secundariaRG,
                    'nombre_a_cargo_secundariaRG': nombre_a_cargo_secundariaRG
                }
            )

        # Guardar detalles adicionales para instituciones federales
        for institucion_federal in form.cleaned_data['instituciones_federales']:
            numero_movil_federal = self.request.POST.get(f'numero_movil_federal_{institucion_federal.id}')
            nombre_a_cargo_federal = self.request.POST.get(f'nombre_a_cargo_federal_{institucion_federal.id}')
            DetalleInstitucionFederal.objects.update_or_create(
                institucion_federal=institucion_federal,
                comisaria_segundaRG=self.object,
                defaults={
                    'numero_movil_federal': numero_movil_federal,
                    'nombre_a_cargo_federal': nombre_a_cargo_federal
                }
            )    

        messages.success(self.request, 'El código ha sido guardado exitosamente.')
        return super().form_valid(form)
    

#--------------------------vista para ver todos completo cada registro------------------------------------------------------


class ComisariaSegundaRGDetailView(DetailView):
    model = ComisariaSegundaRG
    template_name = 'comisariasriogrande/segundaRG/comisaria_segundaRG_detail.html'
    context_object_name = 'record'


#----------------------------softdelete-------------------------------------------------------------

# En views.py

def eliminar_comisaria_segundaRG(request, pk):
    # Obtén el registro a eliminar
    comisaria = get_object_or_404(ComisariaSegundaRG, pk=pk)
    
    # Marca el registro como inactivo
    comisaria.activo = False
    comisaria.save()
    
    # Envía un mensaje de confirmación
    messages.success(request, 'El código ha sido eliminado correctamente.')
    
    # Redirige de vuelta a la lista
    return redirect('comisaria_segundaRG_list')



#-------------------------VISTA DE COMISARIA TERCERARG ---------------------------------------------------------------------------------------------------------


class ComisariaTerceraRGListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ComisariaTerceraRG
    template_name = 'comisariasriogrande/terceraRG/comisaria_terceraRG_list.html'
    context_object_name = 'records'

    def test_func(self): 
        return user_is_in_group(self.request.user, 'comisariaterceraRG')

    def handle_no_permission(self):
        return redirect('no_permission')
    
    def get_paginate_by(self, queryset):
        # Determina cuántos elementos se mostrarán por página, según un parámetro GET.

        items_per_page = self.request.GET.get('items_per_page', 10)  # Obtiene el valor de `items_per_page` (o 10 por defecto).
        try:
            return int(items_per_page)  # Intenta convertir el valor a entero.
        except ValueError:
            return 10  # Si ocurre un error, devuelve el valor por defecto (10).


    def get_queryset(self):
        #queryset = super().get_queryset().order_by('-fecha_hora')
        queryset = super().get_queryset().filter(activo=True).order_by('-fecha_hora')
        search_query = self.request.GET.get('q', '')
        
 # Si hay una consulta de búsqueda, filtra el queryset por coincidencias en el campo 'cuarto'----09/01/25.
        if search_query:  # Verifica si se ingresó un término de búsqueda.
            try:
                search_date = datetime.strptime(search_query, "%d/%m/%Y").date()  
                # Intenta convertir la consulta a una fecha (sin hora) usando el formato 'dd/mm/yyyy'.
                queryset = queryset.filter(fecha_hora__date=search_date)  
                # Filtra los registros donde solo la fecha (sin hora) coincide.
            except (ValueError, TypeError):  
                # Si la consulta no es una fecha válida, realiza el filtrado en otros campos.
                queryset = queryset.filter(
                       Q(codigoRG__codigoRG__icontains=search_query) |
                        Q(codigoRG__nombre_codigo__icontains=search_query) |
                        Q(movil_patrulla__icontains=search_query) |
                        Q(a_cargo__icontains=search_query) |
                        Q(secundante__icontains=search_query) |
                        Q(lugar_codigo__icontains=search_query) |
                        Q(tareas_judiciales__icontains=search_query) |
                        Q(descripcion__icontains=search_query) |
                        Q(fecha_hora__icontains=search_query)
                    )

        return queryset
    #cierre --09/01/25
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['is_jefessuperiores'] = user.groups.filter(name='jefessuperiores').exists()
        context['is_libreros'] = user.groups.filter(name='libreros').exists()
        context['is_encargadosguardias'] = user.groups.filter(name='encargadosguardias').exists()
        context['is_oficialesservicios'] = user.groups.filter(name='oficialesservicios').exists()
        context['is_comisariaterceraRG'] = user.groups.filter(name='comisariatercera').exists()

        context['today'] = timezone.now().date()
        context['resolveId'] = None
    #--paginado--9/01/25
        queryset = self.get_queryset()  # Obtiene el conjunto de datos filtrado.
        paginate_by = self.get_paginate_by(queryset)  # Determina el número de registros por página.
        paginator = Paginator(queryset, paginate_by)  # Crea el objeto de paginación con el conjunto de datos.
        page = self.request.GET.get('page')  # Obtiene el número de la página actual desde los parámetros GET.

        try:
            page_obj = paginator.page(page)  # Obtiene los registros correspondientes a la página actual.
        except PageNotAnInteger:
            page_obj = paginator.page(1)  # Si el número de página no es válido, muestra la primera página.
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)  # Si el número de página está fuera de rango, muestra la última página.

        current_page = page_obj.number  # Obtiene el número de la página actual.
        total_pages = page_obj.paginator.num_pages  # Calcula el número total de páginas.
        range_start = max(current_page - 5, 1)  # Calcula el inicio del rango dinámico de paginación.
        range_end = min(current_page + 5, total_pages) + 1  # Calcula el final del rango dinámico de paginación.

        context['page_obj'] = page_obj  # Añade el objeto de paginación al contexto.
        context['query'] = self.request.GET.get('q', '')  # Añade la consulta de búsqueda al contexto.
        context['items_per_page'] = paginate_by  # Añade el número de elementos por página al contexto.
        context['page_range'] = range(range_start, range_end)  # Añade el rango dinámico de páginas al contexto.

        return context
    #--cierre----09/01/25

#----------------------------CREACION DE COMISARIA TERCERARG----------------------------------------


class ComisariaTerceraRGCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ComisariaTerceraRG
    form_class = ComisariaTerceraRGForm
    template_name = 'comisariasriogrande/terceraRG/comisaria_terceraRG_form.html'
    success_url = reverse_lazy('comisaria_terceraRG_list')

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariaterceraRG')

    def handle_no_permission(self):
        return redirect('no_permission')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['codigos_policialesRG'] = CodigoPolicialRG.objects.all()

        # Inicializar detalles como listas vacías en el contexto
        context['detalle_servicios_emergenciaRG'] = json.dumps([])  # Para vista de creación, siempre es una lista vacía
        context['detalle_instituciones_hospitalariasRG'] = json.dumps([])
        context['detalle_dependencias_municipalesRG'] = json.dumps([])
        context['detalle_dependencias_provincialesRG'] = json.dumps([])
        context['detalle_dependencias_secundariasRG'] = json.dumps([])
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
        for servicioRG in form.cleaned_data['servicios_emergenciaRG']:
            numero_movil_bomberosRG = self.request.POST.get(f'numero_movil_bomberos_{servicioRG.id}')
            nombre_a_cargo_bomberosRG = self.request.POST.get(f'nombre_a_cargo_bomberos_{servicioRG.id}')
            if numero_movil_bomberosRG or nombre_a_cargo_bomberosRG:
                DetalleServicioEmergenciaRG.objects.create(
                    servicio_emergenciaRG=servicioRG,
                    comisaria_terceraRG=self.object,
                    numero_movil_bomberosRG=numero_movil_bomberosRG,
                    nombre_a_cargo_bomberosRG=nombre_a_cargo_bomberosRG
                )

        # Guardar los detalles adicionales para cada institución hospitalaria
        for institucionRG in form.cleaned_data['instituciones_hospitalariasRG']:
            numero_movil_hospitalRG = self.request.POST.get(f'numero_movil_hospital_{institucionRG.id}')
            nombre_a_cargo_hospitalRG = self.request.POST.get(f'nombre_a_cargo_hospital_{institucionRG.id}')
            if numero_movil_hospitalRG or nombre_a_cargo_hospitalRG:
                DetalleInstitucionHospitalariaRG.objects.create(
                    institucion_hospitalariaRG=institucionRG,
                    comisaria_terceraRG=self.object,
                    numero_movil_hospitalRG=numero_movil_hospitalRG,
                    nombre_a_cargo_hospitalRG=nombre_a_cargo_hospitalRG
                )

        # Guardar los detalles adicionales para cada dependencia municipal
        for dependencia_municipalRG in form.cleaned_data['dependencias_municipalesRG']:
            numero_movil_municipalRG = self.request.POST.get(f'numero_movil_municipal_{dependencia_municipalRG.id}')
            nombre_a_cargo_municipalRG = self.request.POST.get(f'nombre_a_cargo_municipal_{dependencia_municipalRG.id}')
            if numero_movil_municipalRG or nombre_a_cargo_municipalRG:
                DetalleDependenciaMunicipalRG.objects.create(
                    dependencia_municipalRG=dependencia_municipalRG,
                    comisaria_terceraRG=self.object,
                    numero_movil_municipalRG=numero_movil_municipalRG,
                    nombre_a_cargo_municipalRG=nombre_a_cargo_municipalRG
                )

        # Guardar los detalles adicionales para cada dependencia provincial
        for dependencia_provincialRG in form.cleaned_data['dependencias_provincialesRG']:
            numero_movil_provincialRG = self.request.POST.get(f'numero_movil_provincial_{dependencia_provincialRG.id}')
            nombre_a_cargo_provincialRG = self.request.POST.get(f'nombre_a_cargo_provincial_{dependencia_provincialRG.id}')
            if numero_movil_provincialRG or nombre_a_cargo_provincialRG:
                DetalleDependenciaProvincialRG.objects.create(
                    dependencia_provincialRG=dependencia_provincialRG,
                    comisaria_terceraRG=self.object,
                    numero_movil_provincialRG=numero_movil_provincialRG,
                    nombre_a_cargo_provincialRG=nombre_a_cargo_provincialRG
                )

        # Guardar los detalles adicionales para dependencias secundarias
        for dependencia_secundariaRG in form.cleaned_data['dependencias_secundariasRG']:
            numero_movil_secundariaRG = self.request.POST.get(f'numero_movil_secundaria_{dependencia_secundariaRG.id}')
            nombre_a_cargo_secundariaRG = self.request.POST.get(f'nombre_a_cargo_secundaria_{dependencia_secundariaRG.id}')
            if numero_movil_secundariaRG or nombre_a_cargo_secundariaRG:
                DetalleDependenciaSecundariaRG.objects.create(
                    dependencia_secundariaRG=dependencia_secundariaRG,
                    comisaria_terceraRG=self.object,
                    numero_movil_secundariaRG=numero_movil_secundariaRG,
                    nombre_a_cargo_secundariaRG=nombre_a_cargo_secundariaRG
                )

        # Guardar los detalles adicionales para instituciones federales
        for institucion_federal in form.cleaned_data['instituciones_federales']:
            numero_movil_federal = self.request.POST.get(f'numero_movil_federal_{institucion_federal.id}')
            nombre_a_cargo_federal = self.request.POST.get(f'nombre_a_cargo_federal_{institucion_federal.id}')
            if numero_movil_federal or nombre_a_cargo_federal:
                DetalleInstitucionFederal.objects.create(
                    institucion_federal=institucion_federal,
                    comisaria_terceraRG=self.object,
                    numero_movil_federal=numero_movil_federal,
                    nombre_a_cargo_federal=nombre_a_cargo_federal
                )

        messages.success(self.request, 'El código ha sido guardado exitosamente.')
        return super().form_valid(form)



#---------------------------------------upadate de comisaria terceraRG-------------------------------------


class ComisariaTerceraRGUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ComisariaTerceraRG
    form_class = ComisariaTerceraRGForm
    template_name = 'comisariasriogrande/terceraRG/comisaria_terceraRG_form.html'
    success_url = reverse_lazy('comisaria_terceraRG_list')

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariaterceraRG')

    def handle_no_permission(self):
        return redirect('no_permission')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        now = timezone.now()

        if obj.fecha_hora.date() != now.date() and not obj.estado:
            return redirect('comisaria_terceraRG_list')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['codigos_policialesRG'] = CodigoPolicialRG.objects.all()

        # Convertir detalles en JSON para ser usados por Alpine.js
        context['detalle_servicios_emergenciaRG'] = json.dumps(list(
            DetalleServicioEmergenciaRG.objects.filter(comisaria_terceraRG=self.object.pk).values('id', 'servicio_emergenciaRG_id', 'numero_movil_bomberosRG', 'nombre_a_cargo_bomberosRG')
        ))

        context['detalle_instituciones_hospitalariasRG'] = json.dumps(list(
            DetalleInstitucionHospitalariaRG.objects.filter(comisaria_terceraRG=self.object.pk).values('id', 'institucion_hospitalariaRG_id', 'numero_movil_hospitalRG', 'nombre_a_cargo_hospitalRG')
        ))

        context['detalle_dependencias_municipalesRG'] = json.dumps(list(
            DetalleDependenciaMunicipalRG.objects.filter(comisaria_terceraRG=self.object.pk).values('id', 'dependencia_municipalRG_id', 'numero_movil_municipalRG', 'nombre_a_cargo_municipalRG')
        ))

        context['detalle_dependencias_provincialesRG'] = json.dumps(list(
            DetalleDependenciaProvincialRG.objects.filter(comisaria_terceraRG=self.object.pk).values('id', 'dependencia_provincialRG_id', 'numero_movil_provincialRG', 'nombre_a_cargo_provincialRG')
        ))

        # Añadir los nuevos detalles para dependencias secundarias
        context['detalle_dependencias_secundariasRG'] = json.dumps(list(
            DetalleDependenciaSecundariaRG.objects.filter(comisaria_terceraRG=self.object.pk).values('id', 'dependencia_secundariaRG_id', 'numero_movil_secundariaRG', 'nombre_a_cargo_secundariaRG')
        ))

        # Añadir los nuevos detalles para instituciones federales
        context['detalle_instituciones_federales'] = json.dumps(list(
            DetalleInstitucionFederal.objects.filter(comisaria_terceraRG=self.object.pk).values('id', 'institucion_federal_id', 'numero_movil_federal', 'nombre_a_cargo_federal')
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
        servicios_emergencia_ids = form.cleaned_data['servicios_emergenciaRG'].values_list('id', flat=True)
        instituciones_hospitalarias_ids = form.cleaned_data['instituciones_hospitalariasRG'].values_list('id', flat=True)
        dependencias_municipales_ids = form.cleaned_data['dependencias_municipalesRG'].values_list('id', flat=True)
        dependencias_provinciales_ids = form.cleaned_data['dependencias_provincialesRG'].values_list('id', flat=True)
        dependencias_secundarias_ids = form.cleaned_data['dependencias_secundariasRG'].values_list('id', flat=True)
        instituciones_federales_ids = form.cleaned_data['instituciones_federales'].values_list('id', flat=True)

        # Eliminar los detalles que ya no están seleccionados
        DetalleServicioEmergenciaRG.objects.filter(comisaria_terceraRG=self.object).exclude(servicio_emergenciaRG_id__in=servicios_emergencia_ids).delete()
        DetalleInstitucionHospitalariaRG.objects.filter(comisaria_terceraRG=self.object).exclude(institucion_hospitalariaRG_id__in=instituciones_hospitalarias_ids).delete()
        DetalleDependenciaMunicipalRG.objects.filter(comisaria_terceraRG=self.object).exclude(dependencia_municipalRG_id__in=dependencias_municipales_ids).delete()
        DetalleDependenciaProvincialRG.objects.filter(comisaria_terceraRG=self.object).exclude(dependencia_provincialRG_id__in=dependencias_provinciales_ids).delete()
        DetalleDependenciaSecundariaRG.objects.filter(comisaria_terceraRG=self.object).exclude(dependencia_secundariaRG_id__in=dependencias_secundarias_ids).delete()
        DetalleInstitucionFederal.objects.filter(comisaria_terceraRG=self.object).exclude(institucion_federal_id__in=instituciones_federales_ids).delete()


        # Guardar los detalles adicionales para cada servicio de emergencia.
        for servicioRG in form.cleaned_data['servicios_emergenciaRG']:
            numero_movil_bomberosRG = self.request.POST.get(f'numero_movil_bomberos_{servicioRG.id}')
            nombre_a_cargo_bomberosRG = self.request.POST.get(f'nombre_a_cargo_bomberos_{servicioRG.id}')
            DetalleServicioEmergenciaRG.objects.update_or_create(
                servicio_emergenciaRG=servicioRG,
                comisaria_terceraRG=self.object,
                defaults={
                    'numero_movil_bomberosRG': numero_movil_bomberosRG,
                    'nombre_a_cargo_bomberosRG': nombre_a_cargo_bomberosRG
                }
            )

        # Guardar los detalles adicionales para cada institución hospitalaria
        for institucionRG in form.cleaned_data['instituciones_hospitalariasRG']:
            numero_movil_hospitalRG = self.request.POST.get(f'numero_movil_hospital_{institucionRG.id}')
            nombre_a_cargo_hospitalRG = self.request.POST.get(f'nombre_a_cargo_hospital_{institucionRG.id}')
            DetalleInstitucionHospitalariaRG.objects.update_or_create(
                institucion_hospitalariaRG=institucionRG,
                comisaria_terceraRG=self.object,
                defaults={
                    'numero_movil_hospitalRG': numero_movil_hospitalRG,
                    'nombre_a_cargo_hospitalRG': nombre_a_cargo_hospitalRG
                }
            )

        # Guardar los detalles adicionales para cada dependencia municipal
        for dependencia_municipalRG in form.cleaned_data['dependencias_municipalesRG']:
            numero_movil_municipalRG = self.request.POST.get(f'numero_movil_municipal_{dependencia_municipalRG.id}')
            nombre_a_cargo_municipalRG = self.request.POST.get(f'nombre_a_cargo_municipal_{dependencia_municipalRG.id}')
            DetalleDependenciaMunicipalRG.objects.update_or_create(
                dependencia_municipalRG=dependencia_municipalRG,
                comisaria_terceraRG=self.object,
                defaults={
                    'numero_movil_municipalRG': numero_movil_municipalRG,
                    'nombre_a_cargo_municipalRG': nombre_a_cargo_municipalRG
                }
            )

        # Guardar los detalles adicionales para cada dependencia provincial
        for dependencia_provincialRG in form.cleaned_data['dependencias_provincialesRG']:
            numero_movil_provincialRG = self.request.POST.get(f'numero_movil_provincial_{dependencia_provincialRG.id}')
            nombre_a_cargo_provincialRG = self.request.POST.get(f'nombre_a_cargo_provincial_{dependencia_provincialRG.id}')
            DetalleDependenciaProvincialRG.objects.update_or_create(
                dependencia_provincialRG=dependencia_provincialRG,
                comisaria_terceraRG=self.object,
                defaults={
                    'numero_movil_provincialRG': numero_movil_provincialRG,
                    'nombre_a_cargo_provincialRG': nombre_a_cargo_provincialRG
                }
            )

        # Guardar detalles adicionales para cada dependencia secundaria
        for dependencia_secundariaRG in form.cleaned_data['dependencias_secundariasRG']:
            numero_movil_secundariaRG = self.request.POST.get(f'numero_movil_secundaria_{dependencia_secundariaRG.id}')
            nombre_a_cargo_secundariaRG = self.request.POST.get(f'nombre_a_cargo_secundaria_{dependencia_secundariaRG.id}')
            DetalleDependenciaSecundariaRG.objects.update_or_create(
                dependencia_secundariaRG=dependencia_secundariaRG,
                comisaria_terceraRG=self.object,
                defaults={
                    'numero_movil_secundariaRG': numero_movil_secundariaRG,
                    'nombre_a_cargo_secundariaRG': nombre_a_cargo_secundariaRG
                }
            )

        # Guardar detalles adicionales para instituciones federales
        for institucion_federal in form.cleaned_data['instituciones_federales']:
            numero_movil_federal = self.request.POST.get(f'numero_movil_federal_{institucion_federal.id}')
            nombre_a_cargo_federal = self.request.POST.get(f'nombre_a_cargo_federal_{institucion_federal.id}')
            DetalleInstitucionFederal.objects.update_or_create(
                institucion_federal=institucion_federal,
                comisaria_terceraRG=self.object,
                defaults={
                    'numero_movil_federal': numero_movil_federal,
                    'nombre_a_cargo_federal': nombre_a_cargo_federal
                }
            )

        messages.success(self.request, 'El código ha sido guardado exitosamente.')
        return super().form_valid(form)


#--------------------------vista para ver todos completo cada registro------------------------------------------------------



class ComisariaTerceraRGDetailView(DetailView):
    model = ComisariaTerceraRG
    template_name = 'comisariasriogrande/terceraRG/comisaria_terceraRG_detail.html'
    context_object_name = 'record'


#----------------------------softdelete-------------------------------------------------------------

# En views.py

def eliminar_comisaria_terceraRG(request, pk):
    # Obtén el registro a eliminar
    comisaria = get_object_or_404(ComisariaTerceraRG, pk=pk)
    
    # Marca el registro como inactivo
    comisaria.activo = False
    comisaria.save()
    
    # Envía un mensaje de confirmación
    messages.success(request, 'El código ha sido eliminado correctamente.')
    
    # Redirige de vuelta a la lista
    return redirect('comisaria_terceraRG_list')



#--------------------------vista para para la comisaria cuartaRG------------------------------------------------------



class ComisariaCuartaRGListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ComisariaCuartaRG
    template_name = 'comisariasriogrande/cuartaRG/comisaria_cuartaRG_list.html'
    context_object_name = 'records'

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariacuartaRG')

    def handle_no_permission(self):
        return redirect('no_permission')
    #funcion paginado--9/01/25
    def get_paginate_by(self, queryset):
        # Determina cuántos elementos se mostrarán por página, según un parámetro GET.

        items_per_page = self.request.GET.get('items_per_page', 10)  # Obtiene el valor de `items_per_page` (o 10 por defecto).
        try:
            return int(items_per_page)  # Intenta convertir el valor a entero.
        except ValueError:
            return 10  # Si ocurre un error, devuelve el valor por defecto (10).
    #--cierre----09/01/25

    def get_queryset(self):
        queryset = super().get_queryset().filter(activo=True).order_by('-fecha_hora')
        #queryset = super().get_queryset().order_by('-fecha_hora')
        search_query = self.request.GET.get('q', '')
      # Si hay una consulta de búsqueda, filtra el queryset por coincidencias en el campo 'cuarto'--9/01/25.
        if search_query:  # Verifica si se ingresó un término de búsqueda.
            try:
                search_date = datetime.strptime(search_query, "%d/%m/%Y").date()  
                # Intenta convertir la consulta a una fecha (sin hora) usando el formato 'dd/mm/yyyy'.
                queryset = queryset.filter(fecha_hora__date=search_date)  
                # Filtra los registros donde solo la fecha (sin hora) coincide.
            except (ValueError, TypeError):  
                # Si la consulta no es una fecha válida, realiza el filtrado en otros campos.
                queryset = queryset.filter(
                       Q(codigoRG__codigoRG__icontains=search_query) |
                        Q(codigoRG__nombre_codigo__icontains=search_query) |
                        Q(movil_patrulla__icontains=search_query) |
                        Q(a_cargo__icontains=search_query) |
                        Q(secundante__icontains=search_query) |
                        Q(lugar_codigo__icontains=search_query) |
                        Q(tareas_judiciales__icontains=search_query) |
                        Q(descripcion__icontains=search_query) |
                        Q(fecha_hora__icontains=search_query)
                    )
            
        return queryset
    #--cierre----09/01/25
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['is_jefessuperiores'] = user.groups.filter(name='jefessuperiores').exists()
        context['is_libreros'] = user.groups.filter(name='libreros').exists()
        context['is_encargadosguardias'] = user.groups.filter(name='encargadosguardias').exists()
        context['is_oficialesservicios'] = user.groups.filter(name='oficialesservicios').exists()
        context['is_comisariacuartaRG'] = user.groups.filter(name='comisariacuartaRG').exists()

        context['today'] = timezone.now().date()
        context['resolveId'] = None

       #paginado--9/01/25
        queryset = self.get_queryset()  # Obtiene el conjunto de datos filtrado.
        paginate_by = self.get_paginate_by(queryset)  # Determina el número de registros por página.
        paginator = Paginator(queryset, paginate_by)  # Crea el objeto de paginación con el conjunto de datos.
        page = self.request.GET.get('page')  # Obtiene el número de la página actual desde los parámetros GET.

        try:
            page_obj = paginator.page(page)  # Obtiene los registros correspondientes a la página actual.
        except PageNotAnInteger:
            page_obj = paginator.page(1)  # Si el número de página no es válido, muestra la primera página.
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)  # Si el número de página está fuera de rango, muestra la última página.

        current_page = page_obj.number  # Obtiene el número de la página actual.
        total_pages = page_obj.paginator.num_pages  # Calcula el número total de páginas.
        range_start = max(current_page - 5, 1)  # Calcula el inicio del rango dinámico de paginación.
        range_end = min(current_page + 5, total_pages) + 1  # Calcula el final del rango dinámico de paginación.

        context['page_obj'] = page_obj  # Añade el objeto de paginación al contexto.
        context['query'] = self.request.GET.get('q', '')  # Añade la consulta de búsqueda al contexto.
        context['items_per_page'] = paginate_by  # Añade el número de elementos por página al contexto.
        context['page_range'] = range(range_start, range_end)  # Añade el rango dinámico de páginas al contexto.


        return context
    #--cierre----09/01/25
    

#----------------------Creacion de comisaria cuartaRG------------------------------------------------------------

class ComisariaCuartaRGCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ComisariaCuartaRG
    form_class = ComisariaCuartaRGForm
    template_name = 'comisariasriogrande/cuartaRG/comisaria_cuartaRG_form.html'
    success_url = reverse_lazy('comisaria_cuartaRG_list')

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariacuartaRG')

    def handle_no_permission(self):
        return redirect('no_permission')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['codigos_policialesRG'] = CodigoPolicialRG.objects.all()

        # Inicializar detalles como listas vacías en el contexto
        context['detalle_servicios_emergenciaRG'] = json.dumps([])  # Para vista de creación, siempre es una lista vacía
        context['detalle_instituciones_hospitalariasRG'] = json.dumps([])
        context['detalle_dependencias_municipalesRG'] = json.dumps([])
        context['detalle_dependencias_provincialesRG'] = json.dumps([])
        context['detalle_dependencias_secundariasRG'] = json.dumps([])
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
        for servicioRG in form.cleaned_data['servicios_emergenciaRG']:
            numero_movil_bomberosRG = self.request.POST.get(f'numero_movil_bomberos_{servicioRG.id}')
            nombre_a_cargo_bomberosRG = self.request.POST.get(f'nombre_a_cargo_bomberos_{servicioRG.id}')
            if numero_movil_bomberosRG or nombre_a_cargo_bomberosRG:
                DetalleServicioEmergenciaRG.objects.create(
                    servicio_emergenciaRG=servicioRG,
                    comisaria_cuartaRG=self.object,
                    numero_movil_bomberosRG=numero_movil_bomberosRG,
                    nombre_a_cargo_bomberosRG=nombre_a_cargo_bomberosRG
                )

        # Guardar los detalles adicionales para cada institución hospitalaria
        for institucionRG in form.cleaned_data['instituciones_hospitalariasRG']:
            numero_movil_hospitalRG = self.request.POST.get(f'numero_movil_hospital_{institucionRG.id}')
            nombre_a_cargo_hospitalRG = self.request.POST.get(f'nombre_a_cargo_hospital_{institucionRG.id}')
            if numero_movil_hospitalRG or nombre_a_cargo_hospitalRG:
                DetalleInstitucionHospitalariaRG.objects.create(
                    institucion_hospitalariaRG=institucionRG,
                    comisaria_cuartaRG=self.object,
                    numero_movil_hospitalRG=numero_movil_hospitalRG,
                    nombre_a_cargo_hospitalRG=nombre_a_cargo_hospitalRG
                )

        # Guardar los detalles adicionales para cada dependencia municipal
        for dependencia_municipalRG in form.cleaned_data['dependencias_municipalesRG']:
            numero_movil_municipalRG = self.request.POST.get(f'numero_movil_municipal_{dependencia_municipalRG.id}')
            nombre_a_cargo_municipalRG = self.request.POST.get(f'nombre_a_cargo_municipal_{dependencia_municipalRG.id}')
            if numero_movil_municipalRG or nombre_a_cargo_municipalRG:
                DetalleDependenciaMunicipalRG.objects.create(
                    dependencia_municipalRG=dependencia_municipalRG,
                    comisaria_cuartaRG=self.object,
                    numero_movil_municipalRG=numero_movil_municipalRG,
                    nombre_a_cargo_municipalRG=nombre_a_cargo_municipalRG
                )

        # Guardar los detalles adicionales para cada dependencia provincial
        for dependencia_provincialRG in form.cleaned_data['dependencias_provincialesRG']:
            numero_movil_provincialRG = self.request.POST.get(f'numero_movil_provincial_{dependencia_provincialRG.id}')
            nombre_a_cargo_provincialRG = self.request.POST.get(f'nombre_a_cargo_provincial_{dependencia_provincialRG.id}')
            if numero_movil_provincialRG or nombre_a_cargo_provincialRG:
                DetalleDependenciaProvincialRG.objects.create(
                    dependencia_provincialRG=dependencia_provincialRG,
                    comisaria_cuartaRG=self.object,
                    numero_movil_provincialRG=numero_movil_provincialRG,
                    nombre_a_cargo_provincialRG=nombre_a_cargo_provincialRG
                )

        # Guardar los detalles adicionales para dependencias secundarias
        for dependencia_secundariaRG in form.cleaned_data['dependencias_secundariasRG']:
            numero_movil_secundariaRG = self.request.POST.get(f'numero_movil_secundaria_{dependencia_secundariaRG.id}')
            nombre_a_cargo_secundariaRG = self.request.POST.get(f'nombre_a_cargo_secundaria_{dependencia_secundariaRG.id}')
            if numero_movil_secundariaRG or nombre_a_cargo_secundariaRG:
                DetalleDependenciaSecundariaRG.objects.create(
                    dependencia_secundariaRG=dependencia_secundariaRG,
                    comisaria_cuartaRG=self.object,
                    numero_movil_secundariaRG=numero_movil_secundariaRG,
                    nombre_a_cargo_secundariaRG=nombre_a_cargo_secundariaRG
                )

        # Guardar los detalles adicionales para instituciones federales
        for institucion_federal in form.cleaned_data['instituciones_federales']:
            numero_movil_federal = self.request.POST.get(f'numero_movil_federal_{institucion_federal.id}')
            nombre_a_cargo_federal = self.request.POST.get(f'nombre_a_cargo_federal_{institucion_federal.id}')
            if numero_movil_federal or nombre_a_cargo_federal:
                DetalleInstitucionFederal.objects.create(
                    institucion_federal=institucion_federal,
                    comisaria_cuartaRG=self.object,
                    numero_movil_federal=numero_movil_federal,
                    nombre_a_cargo_federal=nombre_a_cargo_federal
                )

        messages.success(self.request, 'El código ha sido guardado exitosamente.')
        return super().form_valid(form)
    
  



#--------------------------update comisaria cuartaRG------------------------------------------------------

class ComisariaCuartaRGUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ComisariaCuartaRG
    form_class = ComisariaCuartaRGForm
    template_name = 'comisariasriogrande/cuartaRG/comisaria_cuartaRG_form.html'
    success_url = reverse_lazy('comisaria_cuartaRG_list')

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariacuartaRG')

    def handle_no_permission(self):
        return redirect('no_permission')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        now = timezone.now()

        if obj.fecha_hora.date() != now.date() and not obj.estado:
            return redirect('comisaria_cuartaRG_list')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['codigos_policialesRG'] = CodigoPolicialRG.objects.all()

        # Convertir detalles en JSON para ser usados por Alpine.js
        context['detalle_servicios_emergenciaRG'] = json.dumps(list(
            DetalleServicioEmergenciaRG.objects.filter(comisaria_cuartaRG=self.object.pk).values('id', 'servicio_emergenciaRG_id', 'numero_movil_bomberosRG', 'nombre_a_cargo_bomberosRG')
        ))

        context['detalle_instituciones_hospitalariasRG'] = json.dumps(list(
            DetalleInstitucionHospitalariaRG.objects.filter(comisaria_cuartaRG=self.object.pk).values('id', 'institucion_hospitalariaRG_id', 'numero_movil_hospitalRG', 'nombre_a_cargo_hospitalRG')
        ))

        context['detalle_dependencias_municipalesRG'] = json.dumps(list(
            DetalleDependenciaMunicipalRG.objects.filter(comisaria_cuartaRG=self.object.pk).values('id', 'dependencia_municipalRG_id', 'numero_movil_municipalRG', 'nombre_a_cargo_municipalRG')
        ))

        context['detalle_dependencias_provincialesRG'] = json.dumps(list(
            DetalleDependenciaProvincialRG.objects.filter(comisaria_cuartaRG=self.object.pk).values('id', 'dependencia_provincialRG_id', 'numero_movil_provincialRG', 'nombre_a_cargo_provincialRG')
        ))

        # Añadir los nuevos detalles para dependencias secundarias
        context['detalle_dependencias_secundariasRG'] = json.dumps(list(
            DetalleDependenciaSecundariaRG.objects.filter(comisaria_cuartaRG=self.object.pk).values('id', 'dependencia_secundariaRG_id', 'numero_movil_secundariaRG', 'nombre_a_cargo_secundariaRG')
        ))

        # Añadir los nuevos detalles para instituciones federales
        context['detalle_instituciones_federales'] = json.dumps(list(
            DetalleInstitucionFederal.objects.filter(comisaria_cuartaRG=self.object.pk).values('id', 'institucion_federal_id', 'numero_movil_federal', 'nombre_a_cargo_federal')
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
        servicios_emergencia_ids = form.cleaned_data['servicios_emergenciaRG'].values_list('id', flat=True)
        instituciones_hospitalarias_ids = form.cleaned_data['instituciones_hospitalariasRG'].values_list('id', flat=True)
        dependencias_municipales_ids = form.cleaned_data['dependencias_municipalesRG'].values_list('id', flat=True)
        dependencias_provinciales_ids = form.cleaned_data['dependencias_provincialesRG'].values_list('id', flat=True)
        dependencias_secundarias_ids = form.cleaned_data['dependencias_secundariasRG'].values_list('id', flat=True)
        instituciones_federales_ids = form.cleaned_data['instituciones_federales'].values_list('id', flat=True)
        

        # Eliminar los detalles que ya no están seleccionados
        DetalleServicioEmergenciaRG.objects.filter(comisaria_cuartaRG=self.object).exclude(servicio_emergenciaRG_id__in=servicios_emergencia_ids).delete()
        DetalleInstitucionHospitalariaRG.objects.filter(comisaria_cuartaRG=self.object).exclude(institucion_hospitalariaRG_id__in=instituciones_hospitalarias_ids).delete()
        DetalleDependenciaMunicipalRG.objects.filter(comisaria_cuartaRG=self.object).exclude(dependencia_municipalRG_id__in=dependencias_municipales_ids).delete()
        DetalleDependenciaProvincialRG.objects.filter(comisaria_cuartaRG=self.object).exclude(dependencia_provincialRG_id__in=dependencias_provinciales_ids).delete()
        DetalleDependenciaSecundariaRG.objects.filter(comisaria_cuartaRG=self.object).exclude(dependencia_secundariaRG_id__in=dependencias_secundarias_ids).delete()
        DetalleInstitucionFederal.objects.filter(comisaria_cuartaRG=self.object).exclude(institucion_federal_id__in=instituciones_federales_ids).delete()
        

        # Guardar los detalles adicionales para cada servicio de emergencia.
        for servicioRG in form.cleaned_data['servicios_emergenciaRG']:
            numero_movil_bomberosRG = self.request.POST.get(f'numero_movil_bomberos_{servicioRG.id}')
            nombre_a_cargo_bomberosRG = self.request.POST.get(f'nombre_a_cargo_bomberos_{servicioRG.id}')
            DetalleServicioEmergenciaRG.objects.update_or_create(
                servicio_emergenciaRG=servicioRG,
                comisaria_cuartaRG=self.object,
                defaults={
                    'numero_movil_bomberosRG': numero_movil_bomberosRG,
                    'nombre_a_cargo_bomberosRG': nombre_a_cargo_bomberosRG
                }
            )

        # Guardar los detalles adicionales para cada institución hospitalaria
        for institucionRG in form.cleaned_data['instituciones_hospitalariasRG']:
            numero_movil_hospitalRG = self.request.POST.get(f'numero_movil_hospital_{institucionRG.id}')
            nombre_a_cargo_hospitalRG = self.request.POST.get(f'nombre_a_cargo_hospital_{institucionRG.id}')
            DetalleInstitucionHospitalariaRG.objects.update_or_create(
                institucion_hospitalariaRG=institucionRG,
                comisaria_cuartaRG=self.object,
                defaults={
                    'numero_movil_hospitalRG': numero_movil_hospitalRG,
                    'nombre_a_cargo_hospitalRG': nombre_a_cargo_hospitalRG
                }
            )

        # Guardar los detalles adicionales para cada dependencia municipal
        for dependencia_municipalRG in form.cleaned_data['dependencias_municipalesRG']:
            numero_movil_municipalRG = self.request.POST.get(f'numero_movil_municipal_{dependencia_municipalRG.id}')
            nombre_a_cargo_municipalRG = self.request.POST.get(f'nombre_a_cargo_municipal_{dependencia_municipalRG.id}')
            DetalleDependenciaMunicipalRG.objects.update_or_create(
                dependencia_municipalRG=dependencia_municipalRG,
                comisaria_cuartaRG=self.object,
                defaults={
                    'numero_movil_municipalRG': numero_movil_municipalRG,
                    'nombre_a_cargo_municipalRG': nombre_a_cargo_municipalRG
                }
            )

        # Guardar los detalles adicionales para cada dependencia provincial
        for dependencia_provincialRG in form.cleaned_data['dependencias_provincialesRG']:
            numero_movil_provincialRG = self.request.POST.get(f'numero_movil_provincial_{dependencia_provincialRG.id}')
            nombre_a_cargo_provincialRG = self.request.POST.get(f'nombre_a_cargo_provincial_{dependencia_provincialRG.id}')
            DetalleDependenciaProvincialRG.objects.update_or_create(
                dependencia_provincialRG=dependencia_provincialRG,
                comisaria_cuartaRG=self.object,
                defaults={
                    'numero_movil_provincialRG': numero_movil_provincialRG,
                    'nombre_a_cargo_provincialRG': nombre_a_cargo_provincialRG
                }
            )

        # Guardar detalles adicionales para cada dependencia secundaria
        for dependencia_secundariaRG in form.cleaned_data['dependencias_secundariasRG']:
            numero_movil_secundariaRG = self.request.POST.get(f'numero_movil_secundaria_{dependencia_secundariaRG.id}')
            nombre_a_cargo_secundariaRG = self.request.POST.get(f'nombre_a_cargo_secundaria_{dependencia_secundariaRG.id}')
            DetalleDependenciaSecundariaRG.objects.update_or_create(
                dependencia_secundariaRG=dependencia_secundariaRG,
                comisaria_cuartaRG=self.object,
                defaults={
                    'numero_movil_secundariaRG': numero_movil_secundariaRG,
                    'nombre_a_cargo_secundariaRG': nombre_a_cargo_secundariaRG
                }
            )

        # Guardar detalles adicionales para instituciones federales
        for institucion_federal in form.cleaned_data['instituciones_federales']:
            numero_movil_federal = self.request.POST.get(f'numero_movil_federal_{institucion_federal.id}')
            nombre_a_cargo_federal = self.request.POST.get(f'nombre_a_cargo_federal_{institucion_federal.id}')
            DetalleInstitucionFederal.objects.update_or_create(
                institucion_federal=institucion_federal,
                comisaria_cuartaRG=self.object,
                defaults={
                    'numero_movil_federal': numero_movil_federal,
                    'nombre_a_cargo_federal': nombre_a_cargo_federal
                }
            )

        messages.success(self.request, 'El código ha sido guardado exitosamente.')
        return super().form_valid(form)
    
#--------------------detalle para comisariacuartaRG-------------------------------------  
#    
class ComisariaCuartaRGDetailView(DetailView):
    model = ComisariaCuartaRG
    template_name = 'comisariasriogrande/cuartaRG/comisaria_cuartaRG_detail.html'
    context_object_name = 'record'



#--------------------vista desde la base de datos para comisariacuartaRG-------------------------------------   


from django.db.models import Value, Q, CharField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Vista para listar todas las comisarías de  RG
class ComisariasCuartaRGListView(LoginRequiredMixin, ListView):
    template_name = 'comisariasriogrande/comisarias_completacuartaRG_list.html'
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

        # Filtro de búsqueda
        search_filter = (
            Q(cuartoRG__cuartoRG__icontains=query) |
            Q(codigoRG__codigoRG__icontains=query) |
            Q(codigoRG__nombre_codigo__icontains=query) |
            Q(movil_patrulla__icontains=query) |
            Q(a_cargo__icontains=query) |
            Q(secundante__icontains=query) |
            Q(lugar_codigo__icontains=query) |
            Q(tareas_judiciales__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(fecha_hora__icontains=query)
        ) if query else Q()  # Solo aplica el filtro si hay una consulta

        # Obtiene los datos filtrados
        queryset = ComisariaCuartaRG.objects.filter(
            activo=True
        ).select_related('cuartoRG').filter(search_filter)

        # Ordenar por fecha de creación
        return queryset.order_by('-created_at')

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



#----------------------------softdelete-------------------------------------------------------------

# En views.py

def eliminar_comisaria_cuartaRG(request, pk):
    # Obtén el registro a eliminar
    comisaria = get_object_or_404(ComisariaCuartaRG, pk=pk)
    
    # Marca el registro como inactivo
    comisaria.activo = False
    comisaria.save()
    
    # Envía un mensaje de confirmación
    messages.success(request, 'El código ha sido eliminado correctamente.')
    
    # Redirige de vuelta a la lista
    return redirect('comisaria_cuartaRG_list')





#---------------------comisaria quintaRG para ver ---------------------

class ComisariaQuintaRGListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ComisariaQuintaRG
    template_name = 'comisariasriogrande/quintaRG/comisaria_quintaRG_list.html'
    context_object_name = 'records'

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariaquintaRG')

    def handle_no_permission(self):
        return redirect('no_permission')
    #funcion paginado -9/01/25
    def get_paginate_by(self, queryset):
            # Determina cuántos elementos se mostrarán por página, según un parámetro GET.

            items_per_page = self.request.GET.get('items_per_page', 10)  # Obtiene el valor de `items_per_page` (o 10 por defecto).
            try:
                return int(items_per_page)  # Intenta convertir el valor a entero.
            except ValueError:
                return 10  # Si ocurre un error, devuelve el valor por defecto (10).
    #--cierre----09/01/25            
    def get_queryset(self):
        queryset = super().get_queryset().filter(activo=True).order_by('-fecha_hora')
        #queryset = super().get_queryset().order_by('-fecha_hora')
        search_query = self.request.GET.get('q', '')
       # Si hay una consulta de búsqueda, filtra el queryset por coincidencias en el campo 'cuarto'--9/01/25.
        if search_query:  # Verifica si se ingresó un término de búsqueda.
            try:
                search_date = datetime.strptime(search_query, "%d/%m/%Y").date()  
                # Intenta convertir la consulta a una fecha (sin hora) usando el formato 'dd/mm/yyyy'.
                queryset = queryset.filter(fecha_hora__date=search_date)  
                # Filtra los registros donde solo la fecha (sin hora) coincide.
            except (ValueError, TypeError):  
                # Si la consulta no es una fecha válida, realiza el filtrado en otros campos.
                queryset = queryset.filter(
                       Q(codigoRG__codigoRG__icontains=search_query) |
                       Q(codigoRG__nombre_codigo__icontains=search_query) |
                       Q(movil_patrulla__icontains=search_query) |
                       Q(a_cargo__icontains=search_query) |
                       Q(secundante__icontains=search_query) |
                       Q(lugar_codigo__icontains=search_query) |
                       Q(tareas_judiciales__icontains=search_query) |
                       Q(descripcion__icontains=search_query) |
                       Q(fecha_hora__icontains=search_query)
                    )

        return queryset
    #--cierre----09/01/25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['is_jefessuperiores'] = user.groups.filter(name='jefessuperiores').exists()
        context['is_libreros'] = user.groups.filter(name='libreros').exists()
        context['is_encargadosguardias'] = user.groups.filter(name='encargadosguardias').exists()
        context['is_oficialesservicios'] = user.groups.filter(name='oficialesservicios').exists()
        context['is_comisariaquintaRG'] = user.groups.filter(name='comisariaquintaRG').exists()

        context['today'] = timezone.now().date()
        context['resolveId'] = None
    #paginado 9/01/25
        queryset = self.get_queryset()  # Obtiene el conjunto de datos filtrado.
        paginate_by = self.get_paginate_by(queryset)  # Determina el número de registros por página.
        paginator = Paginator(queryset, paginate_by)  # Crea el objeto de paginación con el conjunto de datos.
        page = self.request.GET.get('page')  # Obtiene el número de la página actual desde los parámetros GET.

        try:
            page_obj = paginator.page(page)  # Obtiene los registros correspondientes a la página actual.
        except PageNotAnInteger:
            page_obj = paginator.page(1)  # Si el número de página no es válido, muestra la primera página.
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)  # Si el número de página está fuera de rango, muestra la última página.

        current_page = page_obj.number  # Obtiene el número de la página actual.
        total_pages = page_obj.paginator.num_pages  # Calcula el número total de páginas.
        range_start = max(current_page - 5, 1)  # Calcula el inicio del rango dinámico de paginación.
        range_end = min(current_page + 5, total_pages) + 1  # Calcula el final del rango dinámico de paginación.

        context['page_obj'] = page_obj  # Añade el objeto de paginación al contexto.
        context['query'] = self.request.GET.get('q', '')  # Añade la consulta de búsqueda al contexto.
        context['items_per_page'] = paginate_by  # Añade el número de elementos por página al contexto.
        context['page_range'] = range(range_start, range_end)  # Añade el rango dinámico de páginas al contexto.

        return context
    #--cierre----09/01/25

#-----------------------creacion de comisaria quintaRG---------------

class ComisariaQuintaRGCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ComisariaQuintaRG
    form_class = ComisariaQuintaRGForm
    template_name = 'comisariasriogrande/quintaRG/comisaria_quintaRG_form.html'
    success_url = reverse_lazy('comisaria_quintaRG_list')

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariaquintaRG')

    def handle_no_permission(self):
        return redirect('no_permission')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['codigos_policialesRG'] = CodigoPolicialRG.objects.all()

        # Inicializar detalles como listas vacías en el contexto
        context['detalle_servicios_emergenciaRG'] = json.dumps([])  # Para vista de creación, siempre es una lista vacía
        context['detalle_instituciones_hospitalariasRG'] = json.dumps([])
        context['detalle_dependencias_municipalesRG'] = json.dumps([])
        context['detalle_dependencias_provincialesRG'] = json.dumps([])
        context['detalle_dependencias_secundariasRG'] = json.dumps([])
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
        for servicioRG in form.cleaned_data['servicios_emergenciaRG']:
            numero_movil_bomberosRG = self.request.POST.get(f'numero_movil_bomberos_{servicioRG.id}')
            nombre_a_cargo_bomberosRG = self.request.POST.get(f'nombre_a_cargo_bomberos_{servicioRG.id}')
            if numero_movil_bomberosRG or nombre_a_cargo_bomberosRG:
                DetalleServicioEmergenciaRG.objects.create(
                    servicio_emergenciaRG=servicioRG,
                    comisaria_quintaRG=self.object,
                    numero_movil_bomberosRG=numero_movil_bomberosRG,
                    nombre_a_cargo_bomberosRG=nombre_a_cargo_bomberosRG
                )

        # Guardar los detalles adicionales para cada institución hospitalaria
        for institucionRG in form.cleaned_data['instituciones_hospitalariasRG']:
            numero_movil_hospitalRG = self.request.POST.get(f'numero_movil_hospital_{institucionRG.id}')
            nombre_a_cargo_hospitalRG = self.request.POST.get(f'nombre_a_cargo_hospital_{institucionRG.id}')
            if numero_movil_hospitalRG or nombre_a_cargo_hospitalRG:
                DetalleInstitucionHospitalariaRG.objects.create(
                    institucion_hospitalariaRG=institucionRG,
                    comisaria_quintaRG=self.object,
                    numero_movil_hospitalRG=numero_movil_hospitalRG,
                    nombre_a_cargo_hospitalRG=nombre_a_cargo_hospitalRG
                )

        # Guardar los detalles adicionales para cada dependencia municipal
        for dependencia_municipalRG in form.cleaned_data['dependencias_municipalesRG']:
            numero_movil_municipalRG = self.request.POST.get(f'numero_movil_municipal_{dependencia_municipalRG.id}')
            nombre_a_cargo_municipalRG = self.request.POST.get(f'nombre_a_cargo_municipal_{dependencia_municipalRG.id}')
            if numero_movil_municipalRG or nombre_a_cargo_municipalRG:
                DetalleDependenciaMunicipalRG.objects.create(
                    dependencia_municipalRG=dependencia_municipalRG,
                    comisaria_quintaRG=self.object,
                    numero_movil_municipalRG=numero_movil_municipalRG,
                    nombre_a_cargo_municipalRG=nombre_a_cargo_municipalRG
                )

        # Guardar los detalles adicionales para cada dependencia provincial
        for dependencia_provincialRG in form.cleaned_data['dependencias_provincialesRG']:
            numero_movil_provincialRG = self.request.POST.get(f'numero_movil_provincial_{dependencia_provincialRG.id}')
            nombre_a_cargo_provincialRG = self.request.POST.get(f'nombre_a_cargo_provincial_{dependencia_provincialRG.id}')
            if numero_movil_provincialRG or nombre_a_cargo_provincialRG:
                DetalleDependenciaProvincialRG.objects.create(
                    dependencia_provincialRG=dependencia_provincialRG,
                    comisaria_quintaRG=self.object,
                    numero_movil_provincialRG=numero_movil_provincialRG,
                    nombre_a_cargo_provincialRG=nombre_a_cargo_provincialRG
                )

        # Guardar los detalles adicionales para dependencias secundarias
        for dependencia_secundariaRG in form.cleaned_data['dependencias_secundariasRG']:
            numero_movil_secundariaRG = self.request.POST.get(f'numero_movil_secundaria_{dependencia_secundariaRG.id}')
            nombre_a_cargo_secundariaRG = self.request.POST.get(f'nombre_a_cargo_secundaria_{dependencia_secundariaRG.id}')
            if numero_movil_secundariaRG or nombre_a_cargo_secundariaRG:
                DetalleDependenciaSecundariaRG.objects.create(
                    dependencia_secundariaRG=dependencia_secundariaRG,
                    comisaria_quintaRG=self.object,
                    numero_movil_secundariaRG=numero_movil_secundariaRG,
                    nombre_a_cargo_secundariaRG=nombre_a_cargo_secundariaRG
                )

        # Guardar los detalles adicionales para instituciones federales
        for institucion_federal in form.cleaned_data['instituciones_federales']:
            numero_movil_federal = self.request.POST.get(f'numero_movil_federal_{institucion_federal.id}')
            nombre_a_cargo_federal = self.request.POST.get(f'nombre_a_cargo_federal_{institucion_federal.id}')
            if numero_movil_federal or nombre_a_cargo_federal:
                DetalleInstitucionFederal.objects.create(
                    institucion_federal=institucion_federal,
                    comisaria_quintaRG=self.object,
                    numero_movil_federal=numero_movil_federal,
                    nombre_a_cargo_federal=nombre_a_cargo_federal
                )

        messages.success(self.request, 'El código ha sido guardado exitosamente.')
        return super().form_valid(form)

#-------------------update de comisaria quintaRG-----------------------------

class ComisariaQuintaRGUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ComisariaQuintaRG
    form_class = ComisariaQuintaRGForm
    template_name = 'comisariasriogrande/quintaRG/comisaria_quintaRG_form.html'
    success_url = reverse_lazy('comisaria_quintaRG_list')

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariaquintaRG')

    def handle_no_permission(self):
        return redirect('no_permission')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        now = timezone.now()

        if obj.fecha_hora.date() != now.date() and not obj.estado:
            return redirect('comisaria_quintaRG_list')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['codigos_policialesRG'] = CodigoPolicialRG.objects.all()

        # Convertir detalles en JSON para ser usados por Alpine.js
        context['detalle_servicios_emergenciaRG'] = json.dumps(list(
            DetalleServicioEmergenciaRG.objects.filter(comisaria_quintaRG=self.object.pk).values('id', 'servicio_emergenciaRG_id', 'numero_movil_bomberosRG', 'nombre_a_cargo_bomberosRG')
        ))

        context['detalle_instituciones_hospitalariasRG'] = json.dumps(list(
            DetalleInstitucionHospitalariaRG.objects.filter(comisaria_quintaRG=self.object.pk).values('id', 'institucion_hospitalariaRG_id', 'numero_movil_hospitalRG', 'nombre_a_cargo_hospitalRG')
        ))

        context['detalle_dependencias_municipalesRG'] = json.dumps(list(
            DetalleDependenciaMunicipalRG.objects.filter(comisaria_quintaRG=self.object.pk).values('id', 'dependencia_municipalRG_id', 'numero_movil_municipalRG', 'nombre_a_cargo_municipalRG')
        ))

        context['detalle_dependencias_provincialesRG'] = json.dumps(list(
            DetalleDependenciaProvincialRG.objects.filter(comisaria_quintaRG=self.object.pk).values('id', 'dependencia_provincialRG_id', 'numero_movil_provincialRG', 'nombre_a_cargo_provincialRG')
        ))

        # Añadir los nuevos detalles para dependencias secundarias
        context['detalle_dependencias_secundariasRG'] = json.dumps(list(
            DetalleDependenciaSecundariaRG.objects.filter(comisaria_quintaRG=self.object.pk).values('id', 'dependencia_secundariaRG_id', 'numero_movil_secundariaRG', 'nombre_a_cargo_secundariaRG')
        ))

        # Añadir los nuevos detalles para instituciones federales
        context['detalle_instituciones_federales'] = json.dumps(list(
            DetalleInstitucionFederal.objects.filter(comisaria_quintaRG=self.object.pk).values('id', 'institucion_federal_id', 'numero_movil_federal', 'nombre_a_cargo_federal')
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
        servicios_emergencia_ids = form.cleaned_data['servicios_emergenciaRG'].values_list('id', flat=True)
        instituciones_hospitalarias_ids = form.cleaned_data['instituciones_hospitalariasRG'].values_list('id', flat=True)
        dependencias_municipales_ids = form.cleaned_data['dependencias_municipalesRG'].values_list('id', flat=True)
        dependencias_provinciales_ids = form.cleaned_data['dependencias_provincialesRG'].values_list('id', flat=True)
        dependencias_secundarias_ids = form.cleaned_data['dependencias_secundariasRG'].values_list('id', flat=True)
        instituciones_federales_ids = form.cleaned_data['instituciones_federales'].values_list('id', flat=True)

        # Eliminar los detalles que ya no están seleccionados
        DetalleServicioEmergenciaRG.objects.filter(comisaria_quintaRG=self.object).exclude(servicio_emergenciaRG_id__in=servicios_emergencia_ids).delete()
        DetalleInstitucionHospitalariaRG.objects.filter(comisaria_quintaRG=self.object).exclude(institucion_hospitalariaRG_id__in=instituciones_hospitalarias_ids).delete()
        DetalleDependenciaMunicipalRG.objects.filter(comisaria_quintaRG=self.object).exclude(dependencia_municipalRG_id__in=dependencias_municipales_ids).delete()
        DetalleDependenciaProvincialRG.objects.filter(comisaria_quintaRG=self.object).exclude(dependencia_provincialRG_id__in=dependencias_provinciales_ids).delete()
        DetalleDependenciaSecundariaRG.objects.filter(comisaria_quintaRG=self.object).exclude(dependencia_secundariaRG_id__in=dependencias_secundarias_ids).delete()
        DetalleInstitucionFederal.objects.filter(comisaria_quintaRG=self.object).exclude(institucion_federal_id__in=instituciones_federales_ids).delete()

        # Guardar los detalles adicionales para cada servicio de emergencia
        for servicioRG in form.cleaned_data['servicios_emergenciaRG']:
            numero_movil_bomberosRG = self.request.POST.get(f'numero_movil_bomberos_{servicioRG.id}')
            nombre_a_cargo_bomberosRG = self.request.POST.get(f'nombre_a_cargo_bomberos_{servicioRG.id}')
            DetalleServicioEmergenciaRG.objects.update_or_create(
                servicio_emergenciaRG=servicioRG,
                comisaria_quintaRG=self.object,
                defaults={
                    'numero_movil_bomberosRG': numero_movil_bomberosRG,
                    'nombre_a_cargo_bomberosRG': nombre_a_cargo_bomberosRG
                }
            )

        # Guardar los detalles adicionales para cada institución hospitalaria
        for institucionRG in form.cleaned_data['instituciones_hospitalariasRG']:
            numero_movil_hospitalRG = self.request.POST.get(f'numero_movil_hospital_{institucionRG.id}')
            nombre_a_cargo_hospitalRG = self.request.POST.get(f'nombre_a_cargo_hospital_{institucionRG.id}')
            DetalleInstitucionHospitalariaRG.objects.update_or_create(
                institucion_hospitalariaRG=institucionRG,
                comisaria_quintaRG=self.object,
                defaults={
                    'numero_movil_hospitalRG': numero_movil_hospitalRG,
                    'nombre_a_cargo_hospitalRG': nombre_a_cargo_hospitalRG
                }
            )

        # Guardar los detalles adicionales para cada dependencia municipal
        for dependencia_municipalRG in form.cleaned_data['dependencias_municipalesRG']:
            numero_movil_municipalRG = self.request.POST.get(f'numero_movil_municipal_{dependencia_municipalRG.id}')
            nombre_a_cargo_municipalRG = self.request.POST.get(f'nombre_a_cargo_municipal_{dependencia_municipalRG.id}')
            DetalleDependenciaMunicipalRG.objects.update_or_create(
                dependencia_municipalRG=dependencia_municipalRG,
                comisaria_quintaRG=self.object,
                defaults={
                    'numero_movil_municipalRG': numero_movil_municipalRG,
                    'nombre_a_cargo_municipalRG': nombre_a_cargo_municipalRG
                }
            )

        # Guardar los detalles adicionales para cada dependencia provincial
        for dependencia_provincialRG in form.cleaned_data['dependencias_provincialesRG']:
            numero_movil_provincialRG = self.request.POST.get(f'numero_movil_provincial_{dependencia_provincialRG.id}')
            nombre_a_cargo_provincialRG = self.request.POST.get(f'nombre_a_cargo_provincial_{dependencia_provincialRG.id}')
            DetalleDependenciaProvincialRG.objects.update_or_create(
                dependencia_provincialRG=dependencia_provincialRG,
                comisaria_quintaRG=self.object,
                defaults={
                    'numero_movil_provincialRG': numero_movil_provincialRG,
                    'nombre_a_cargo_provincialRG': nombre_a_cargo_provincialRG
                }
            )

        # Guardar los detalles adicionales para dependencias secundarias
        for dependencia_secundariaRG in form.cleaned_data['dependencias_secundariasRG']:
            numero_movil_secundariaRG = self.request.POST.get(f'numero_movil_secundaria_{dependencia_secundariaRG.id}')
            nombre_a_cargo_secundariaRG = self.request.POST.get(f'nombre_a_cargo_secundaria_{dependencia_secundariaRG.id}')
            DetalleDependenciaSecundariaRG.objects.update_or_create(
                dependencia_secundariaRG=dependencia_secundariaRG,
                comisaria_quintaRG=self.object,
                defaults={
                    'numero_movil_secundariaRG': numero_movil_secundariaRG,
                    'nombre_a_cargo_secundariaRG': nombre_a_cargo_secundariaRG
                }
            )

        # Guardar los detalles adicionales para instituciones federales
        for institucion_federal in form.cleaned_data['instituciones_federales']:
            numero_movil_federal = self.request.POST.get(f'numero_movil_federal_{institucion_federal.id}')
            nombre_a_cargo_federal = self.request.POST.get(f'nombre_a_cargo_federal_{institucion_federal.id}')
            DetalleInstitucionFederal.objects.update_or_create(
                institucion_federal=institucion_federal,
                comisaria_quintaRG=self.object,
                defaults={
                    'numero_movil_federal': numero_movil_federal,
                    'nombre_a_cargo_federal': nombre_a_cargo_federal
                }
            )

        messages.success(self.request, 'El código ha sido guardado exitosamente.')

        return super().form_valid(form)
    

#--------------------detalle comisria quintaRG---------------------------------------------


class ComisariaQuintaRGDetailView(DetailView):
    model = ComisariaQuintaRG
    template_name = 'comisariasriogrande/quintaRG/comisaria_quintaRG_detail.html'
    context_object_name = 'record'


#----------------------------softdelete-------------------------------------------------------------

# En views.py

def eliminar_comisaria_quintaRG(request, pk):
    # Obtén el registro a eliminar
    comisaria = get_object_or_404(ComisariaQuintaRG, pk=pk)
    
    # Marca el registro como inactivo
    comisaria.activo = False
    comisaria.save()
    
    # Envía un mensaje de confirmación
    messages.success(request, 'El código ha sido eliminado correctamente.')
    
    # Redirige de vuelta a la lista
    return redirect('comisaria_quintaRG_list')



#--------------------vista dee todas las comisariasRG-------------------------------------    
from django.db.models import Value, Q, CharField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Vista para listar todas las comisarías de  RG
class ComisariasCompletaRGListView(LoginRequiredMixin, ListView):
    template_name = 'comisariasriogrande/comisarias_completaRG_list.html'
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
            Q(cuartoRG__cuartoRG__icontains=query) |
            Q(codigoRG__codigoRG__icontains=query) |
            Q(codigoRG__nombre_codigoRG__icontains=query) |
            Q(movil_patrulla__icontains=query) |
            Q(a_cargo__icontains=query) |
            Q(secundante__icontains=query) |
            Q(lugar_codigo__icontains=query) |
            Q(tareas_judiciales__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(fecha_hora__icontains=query)
        ) if query else Q()  # Solo aplica el filtro si hay una consulta

        # Filtra y anota cada QuerySet individualmente
        comisarias_primeraRG = ComisariaPrimeraRG.objects.filter(
            activo=True
        ).select_related('cuartoRG').annotate(
            comisaria_nombre=Value('Comisaria Primera Rio Grande', output_field=CharField())
        ).filter(search_filter)

        comisarias_segundaRG = ComisariaSegundaRG.objects.filter(
            activo=True
        ).select_related('cuartoRG').annotate(
            comisaria_nombre=Value('Comisaria Segunda Rio Grande', output_field=CharField())
        ).filter(search_filter)

        comisarias_terceraRG = ComisariaTerceraRG.objects.filter(
            activo=True
        ).select_related('cuartoRG').annotate(
            comisaria_nombre=Value('Comisaria Tercera Rio Grande', output_field=CharField())
        ).filter(search_filter)

        comisarias_cuartaRG = ComisariaCuartaRG.objects.filter(
            activo=True
        ).select_related('cuartoRG').annotate(
            comisaria_nombre=Value('Comisaria Cuarta Rio Grande', output_field=CharField())
        ).filter(search_filter)

        comisarias_quintaRG = ComisariaQuintaRG.objects.filter(
            activo=True
        ).select_related('cuartoRG').annotate(
            comisaria_nombre=Value('Comisaria Quinta Rio Grande', output_field=CharField())
        ).filter(search_filter)

        # Unión de los QuerySets
        combined_queryset = comisarias_primeraRG.union(
            comisarias_segundaRG,
            comisarias_terceraRG,
            comisarias_cuartaRG,
            comisarias_quintaRG
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
    template = get_template('comisariasriogrande/comisariasRG_pdf_template.html')

    
    # Convierte la imagen a base64
    escudo_path = os.path.join(settings.BASE_DIR, 'comisariasriogrande', 'static', 'comisariasriogrande', 'images', 'ESCUDO POLICIA.jpeg')
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


def generate_comisaria_primeraRG_pdf_view(request):
    # Llama a la función view_pdf_content, pasando el request y el modelo ComisariaPrimera.
    # Esta función generará el contenido del PDF para la ComisariaPrimera y lo devolverá como una respuesta HTTP.
    return view_pdf_content(request, ComisariaPrimeraRG)

def generate_comisaria_primeraRG_pdf_download(request):
    add_signature = 'signature' in request.GET
    now = datetime.now()

  # Guarda el verbose_name original
    original_verbose_name = ComisariaPrimeraRG._meta.verbose_name
    
    # Redefine verbose_name temporalmente
    ComisariaPrimeraRG._meta.verbose_name = "Comisaría Primera Rio Grande"

    # Define el nombre del archivo.
    filename = f"libro-diario-Comisaría-Primera-Rio-Grande-{now.strftime('%d-%m-%Y')}.pdf"
    
    # Llama a generate_pdf
    response = generate_pdf(request, ComisariaPrimeraRG, filename, add_signature=add_signature)

    # Restaura el verbose_name original
    ComisariaPrimeraRG._meta.verbose_name = original_verbose_name

    return response


#------------------------------Descargar PDF del día anterior para Comisaria PrimeraRG----------------------------------------



def generate_comisaria_primeraRG_pdf_download_previous_day(request):
    # Verifica si la URL contiene el parámetro 'signature' en la cadena de consulta (GET).
    add_signature = 'signature' in request.GET
    
    # Obtiene la fecha y hora actual.
    now = datetime.now()

    # Define el nombre de la comisaría sin "RG".
    comisaria_name = "Comisaría Primera Rio Grande"

    # Calcula la fecha del día anterior.
    previous_day = now - timedelta(days=1)
    
    # Define el nombre del archivo para el PDF, incluyendo "libro-diario", 
    # la fecha del día anterior, y la extensión ".pdf".
    filename = f"libro-diario-{comisaria_name}-{previous_day.strftime('%d-%m-%Y')}.pdf"
    
    # Genera el PDF para la fecha específica y lo devuelve como una respuesta HTTP.
    return generate_pdf_for_specific_date(request, ComisariaPrimeraRG, previous_day, filename, add_signature=add_signature)  


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
    template = get_template('comisariasriogrande/comisariasRG_pdf_template.html')
    
    # Convierte la imagen a base64
    escudo_path = os.path.join(settings.BASE_DIR, 'comisariasriogrande', 'static', 'comisariasriogrande', 'images', 'ESCUDO POLICIA.jpeg')
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

def subir_pdfRG(request):
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
                folder = 'partespdfRG/'
                fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, folder))
                filename = fs.save(pdf.name, pdf)
                new_pdf = UploadedPDFRG(file=os.path.join(folder, filename), uploaded_by=request.user)
                new_pdf.save()
                return JsonResponse({'success': 'El archivo PDF se ha subido correctamente.'})
            except Exception as e:
                return JsonResponse({'error': f'Error al subir el archivo: {str(e)}'})
        else:
            return JsonResponse({'error': 'No se seleccionó ningún archivo.'})
    return render(request, 'comisariasriogrande/subir_pdfRG.html')


#-----------------------------------funcion para ver todos los registros  de los pdfRG--------------------------------------------------------------



from django.http import FileResponse

def ver_pdfsRG(request):
    # Obtiene todos los registros de PDF almacenados en la base de datos
    pdfs = UploadedPDFRG.objects.all()
    
    # Renderiza la plantilla 'ver_pdfsRG.html' y pasa los registros de PDF al contexto
    return render(request, 'comisariasriogrande/ver_pdfsRG.html', {'pdfs': pdfs})

def mostrar_pdfRG(request, pdf_id):
    # Obtiene el objeto UploadedPDFRG por ID
    pdf = UploadedPDFRG.objects.get(id=pdf_id)
    
    # Abre el archivo desde el sistema de archivos
    pdf_path = pdf.file.path
    response = FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')
    
    # Asegúrate de que el PDF se abra en el navegador en lugar de descargarse
    response['Content-Disposition'] = 'inline; filename="%s"' % pdf.file.name
    
    return response


#-----------------------aqui empieza las funciones de comisarias segundaRG----------------------------------------------------


# Repite las siguientes funciones para las demás comisarías...
def generate_comisaria_segundaRG_pdf_view(request):
    return view_pdf_content(request, ComisariaSegundaRG)

def generate_comisaria_segundaRG_pdf_download(request):
    add_signature = 'signature' in request.GET
    now = datetime.now()

  # Guarda el verbose_name original
    original_verbose_name = ComisariaSegundaRG._meta.verbose_name
    
    # Redefine verbose_name temporalmente
    ComisariaSegundaRG._meta.verbose_name = "Comisaría Segunda Rio Grande"

    # Define el nombre del archivo.
    filename = f"libro-diario-Comisaría-Segunda-Rio-Grande-{now.strftime('%d-%m-%Y')}.pdf"
    
    # Llama a generate_pdf
    response = generate_pdf(request, ComisariaSegundaRG, filename, add_signature=add_signature)

    # Restaura el verbose_name original
    ComisariaSegundaRG._meta.verbose_name = original_verbose_name

    return response


#------------------------------Descargar PDF del día anterior para Comisaria SegundaRG----------------------------------------



def generate_comisaria_segundaRG_pdf_download_previous_day(request):
    # Verifica si la URL contiene el parámetro 'signature' en la cadena de consulta (GET).
    add_signature = 'signature' in request.GET
    
    # Obtiene la fecha y hora actual.
    now = datetime.now()

    # Define el nombre de la comisaría sin "RG".
    comisaria_name = "Comisaría Segunda Rio Grande"

    # Calcula la fecha del día anterior.
    previous_day = now - timedelta(days=1)
    
    # Define el nombre del archivo para el PDF, incluyendo "libro-diario", 
    # la fecha del día anterior, y la extensión ".pdf".
    filename = f"libro-diario-{comisaria_name}-{previous_day.strftime('%d-%m-%Y')}.pdf"
    
    # Genera el PDF para la fecha específica y lo devuelve como una respuesta HTTP.
    return generate_pdf_for_specific_date(request, ComisariaSegundaRG, previous_day, filename, add_signature=add_signature)  


#--------------------------aqui empieza comisiaria terceraRG los pdf------------------------------------------------------


def generate_comisaria_terceraRG_pdf_view(request):
    return view_pdf_content(request, ComisariaTerceraRG)

def generate_comisaria_terceraRG_pdf_download(request):
    add_signature = 'signature' in request.GET
    now = datetime.now()

  # Guarda el verbose_name original
    original_verbose_name = ComisariaTerceraRG._meta.verbose_name
    
    # Redefine verbose_name temporalmente
    ComisariaTerceraRG._meta.verbose_name = "Comisaría Tercera Rio Grande"

    # Define el nombre del archivo.
    filename = f"libro-diario-Comisaría-Tercera-Rio-Grande-{now.strftime('%d-%m-%Y')}.pdf"
    
    # Llama a generate_pdf
    response = generate_pdf(request, ComisariaTerceraRG, filename, add_signature=add_signature)

    # Restaura el verbose_name original
    ComisariaTerceraRG._meta.verbose_name = original_verbose_name

    return response


#------------------------------Descargar PDF del día anterior para Comisaria TerceraRG----------------------------------------



def generate_comisaria_terceraRG_pdf_download_previous_day(request):
    # Verifica si la URL contiene el parámetro 'signature' en la cadena de consulta (GET).
    add_signature = 'signature' in request.GET
    
    # Obtiene la fecha y hora actual.
    now = datetime.now()

    # Define el nombre de la comisaría sin "RG".
    comisaria_name = "Comisaría Tercera Rio Grande"

    # Calcula la fecha del día anterior.
    previous_day = now - timedelta(days=1)
    
    # Define el nombre del archivo para el PDF, incluyendo "libro-diario", 
    # la fecha del día anterior, y la extensión ".pdf".
    filename = f"libro-diario-{comisaria_name}-{previous_day.strftime('%d-%m-%Y')}.pdf"
    
    # Genera el PDF para la fecha específica y lo devuelve como una respuesta HTTP.
    return generate_pdf_for_specific_date(request, ComisariaTerceraRG, previous_day, filename, add_signature=add_signature)  



#-----------------------aqui empieza comisaria cuartaRG las funciones pdf ---------------------------------------------

def generate_comisaria_cuartaRG_pdf_view(request):
    return view_pdf_content(request, ComisariaCuartaRG)



#------------------------------------------------------------------------------------------------------------------
def generate_comisaria_cuartaRG_pdf_download(request):
    add_signature = 'signature' in request.GET
    now = datetime.now()

  # Guarda el verbose_name original
    original_verbose_name = ComisariaCuartaRG._meta.verbose_name
    
    # Redefine verbose_name temporalmente
    ComisariaCuartaRG._meta.verbose_name = "Comisaría Cuarta Rio Grande"

    # Define el nombre del archivo.
    filename = f"libro-diario-Comisaría-Cuarta-Rio-Grande-{now.strftime('%d-%m-%Y')}.pdf"
    
    # Llama a generate_pdf
    response = generate_pdf(request, ComisariaCuartaRG, filename, add_signature=add_signature)

    # Restaura el verbose_name original
    ComisariaCuartaRG._meta.verbose_name = original_verbose_name

    return response


#------------------------------Descargar PDF del día anterior para Comisaria CuartaRG----------------------------------------



def generate_comisaria_cuartaRG_pdf_download_previous_day(request):
    # Verifica si la URL contiene el parámetro 'signature' en la cadena de consulta (GET).
    add_signature = 'signature' in request.GET
    
    # Obtiene la fecha y hora actual.
    now = datetime.now()

    # Define el nombre de la comisaría sin "RG".
    comisaria_name = "Comisaría Cuarta Rio Grande"

    # Calcula la fecha del día anterior.
    previous_day = now - timedelta(days=1)
    
    # Define el nombre del archivo para el PDF, incluyendo "libro-diario", 
    # la fecha del día anterior, y la extensión ".pdf".
    filename = f"libro-diario-{comisaria_name}-{previous_day.strftime('%d-%m-%Y')}.pdf"
    
    # Genera el PDF para la fecha específica y lo devuelve como una respuesta HTTP.
    return generate_pdf_for_specific_date(request, ComisariaCuartaRG, previous_day, filename, add_signature=add_signature)  



#-----------------------aqui empieza comisaria quintaRG las funciones pdf ---------------------------------------------

def generate_comisaria_quintaRG_pdf_view(request):
    return view_pdf_content(request, ComisariaQuintaRG)



#------------------------------------------------------------------------------------------------------------------
def generate_comisaria_quintaRG_pdf_download(request):
    add_signature = 'signature' in request.GET
    now = datetime.now()

  # Guarda el verbose_name original
    original_verbose_name = ComisariaQuintaRG._meta.verbose_name
    
    # Redefine verbose_name temporalmente
    ComisariaQuintaRG._meta.verbose_name = "Comisaría Quinta Rio Grande"

    # Define el nombre del archivo.
    filename = f"libro-diario-Comisaría-Quinta-Rio-Grande-{now.strftime('%d-%m-%Y')}.pdf"
    
    # Llama a generate_pdf
    response = generate_pdf(request, ComisariaQuintaRG, filename, add_signature=add_signature)

    # Restaura el verbose_name original
    ComisariaQuintaRG._meta.verbose_name = original_verbose_name

    return response


#------------------------------Descargar PDF del día anterior para Comisaria QuintaRG----------------------------------------



def generate_comisaria_quintaRG_pdf_download_previous_day(request):
    # Verifica si la URL contiene el parámetro 'signature' en la cadena de consulta (GET).
    add_signature = 'signature' in request.GET
    
    # Obtiene la fecha y hora actual.
    now = datetime.now()

    # Define el nombre de la comisaría sin "RG".
    comisaria_name = "Comisaría Quinta Rio Grande"

    # Calcula la fecha del día anterior.
    previous_day = now - timedelta(days=1)
    
    # Define el nombre del archivo para el PDF, incluyendo "libro-diario", 
    # la fecha del día anterior, y la extensión ".pdf".
    filename = f"libro-diario-{comisaria_name}-{previous_day.strftime('%d-%m-%Y')}.pdf"
    
    # Genera el PDF para la fecha específica y lo devuelve como una respuesta HTTP.
    return generate_pdf_for_specific_date(request, ComisariaQuintaRG, previous_day, filename, add_signature=add_signature)  

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
    template = get_template('comisariasriogrande/comisariasRG_pdf_template.html')  # Ajustar ruta para la nueva app

    # Convertir la imagen a base64
    escudo_path = os.path.join(settings.BASE_DIR, 'comisariasriogrande', 'static', 'comisariasriogrande', 'images', 'ESCUDO POLICIA.jpeg')
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

def generate_pdf_custom_range_view_rg(request):
    # Obtener los valores del formulario
    start_date = request.GET.get('start_date')  # Formato: 'YYYY-MM-DD'
    start_time = request.GET.get('start_time')  # Formato: 'HH:MM'
    end_date = request.GET.get('end_date')      # Formato: 'YYYY-MM-DD'
    end_time = request.GET.get('end_time')      # Formato: 'HH:MM'
    comisaria_name = request.GET.get('comisaria')  # Nombre de la comisaría seleccionada

    # Mapear el nombre de la comisaría al modelo
    comisaria_map = {
        'primera': ComisariaPrimeraRG,
        'segunda': ComisariaSegundaRG,
        'tercera': ComisariaTerceraRG,
        'cuarta': ComisariaCuartaRG,
        'quinta': ComisariaQuintaRG,
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
def select_range_view_rg(request):
    # Renderizar el formulario para seleccionar el rango
    return render(request, 'comisariasriogrande/select_range_riogrande.html')