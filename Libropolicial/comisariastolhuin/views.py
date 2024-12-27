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
from .forms import ComisariaTolhuinForm, CustomLoginForm
from .models import ComisariaTolhuin, DependenciasSecundariasTOL, CodigoPolicialTOL, DetalleDependenciaSecundariaTOL, DetalleInstitucionFederal, DetalleServicioEmergenciaTOL, DetalleInstitucionHospitalariaTOL, DetalleDependenciaMunicipalTOL, DetalleDependenciaProvincialTOL 
from compartido.models import UploadedPDFTOL

from compartido.utils import user_is_in_group
import base64


#------------------funcion par de realizar las firmas--------------------------------------------

@login_required
def sign_comisaria_tolhuin(request, pk):
    # Obtiene la instancia de ComisariaTolhuin correspondiente al ID (pk) proporcionado.
    # Si no se encuentra, lanza una excepción 404.
    comisaria = get_object_or_404(ComisariaTolhuin, pk=pk)
    
    # Obtiene el nombre completo del usuario actual, o su nombre de usuario si el nombre completo no está disponible.
    user_full_name = request.user.get_full_name() or request.user.username
    
    # Verifica si ya hay firmas en la instancia de ComisariaTolhuin.
    if comisaria.firmas:
        # Si ya existen firmas, añade la firma del usuario actual, separada por una coma.
        comisaria.firmas += f", {user_full_name}"
    else:
        # Si no hay firmas previas, establece la firma del usuario actual como la tolhuin firma.
        comisaria.firmas = user_full_name
    
    # Guarda los cambios en la instancia de ComisariaTolhuin, pero solo actualiza el campo 'firmas'.
    comisaria.save(update_fields=['firmas'])  # Solo actualiza el campo firmas
    
    # Redirige al usuario a la vista de la lista de ComisariaTolhuin después de firmar.
    return redirect(reverse('comisaria_tolhuin_list'))
#-------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------

# Función para firmar en Comisaria TolhuinTOL
@login_required
def sign_comisaria_tolhuin(request, pk):
    comisaria = get_object_or_404(ComisariaTolhuin, pk=pk)
    user_full_name = request.user.get_full_name() or request.user.username
    if comisaria.firmas:
        comisaria.firmas += f", {user_full_name}"
    else:
        comisaria.firmas = user_full_name
    comisaria.save(update_fields=['firmas'])  # Solo actualiza el campo firmas
    return redirect(reverse('comisaria_tolhuin_list'))

#--------------------------------------------------------------------------------------------------------
#-------------------clase para ver la tabla los codigos comisariatolhuin filtrando con los permisos-------------------------------------------------------------------------

# views.py

class ComisariaTolhuinListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    # Especifica el modelo de datos que se va a listar.
    model = ComisariaTolhuin
    
    # Define la plantilla que se utilizará para renderizar la lista.
    template_name = 'comisariastolhuin/tolhuin/comisaria_tolhuin_list.html'
    
    # Define el nombre del contexto que contendrá la lista de registros.
    context_object_name = 'records'

    # Método que determina si el usuario tiene permiso para acceder a esta vista.
    def test_func(self):
        # Verifica si el usuario pertenece al grupo 'comisariatolhuin'.
        return user_is_in_group(self.request.user, 'comisariatolhuin')

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
            queryset = queryset.filter(cuartoTOL__cuartoTOL__icontains=search_query)
        
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
          
        
        #context['is_encargados_guardias_tolhuin'] = user.groups.filter(name='encargados_guardias_tolhuin').exists()
        #context['is_jefessuperiores'] = user.groups.filter(name='jefessuperiores').exists()
        #context['is_oficialesservicios'] = user.groups.filter(name='oficialesservicios').exists()
        #context['is_comisariatolhuin'] = user.groups.filter(name='comisariatolhuin').exists()

        context['is_jefessuperiores'] = user.groups.filter(name='jefessuperiores').exists()
        context['is_libreros'] = user.groups.filter(name='libreros').exists()
        context['is_encargadosguardias'] = user.groups.filter(name='encargadosguardias').exists()
        context['is_oficialesservicios'] = user.groups.filter(name='oficialesservicios').exists()
        context['is_comisariatolhuin'] = user.groups.filter(name='comisariatolhuin').exists()
        
        # Agrega la fecha actual al contexto.
        context['today'] = timezone.now().date()
        
        # Inicializa resolveId en None y lo agrega al contexto.
        context['resolveId'] = None  # Inicializa resolveId en None
        
        # Devuelve el contexto completo.
        return context
    
    #---------------------------clase para el create del formulario------------------------------------------------------------------------------------
   


class ComisariaTolhuinCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    # Especifica el modelo de datos que se va a crear.
    model = ComisariaTolhuin
    
    # Especifica el formulario que se utilizará para crear el objeto.
    form_class = ComisariaTolhuinForm
    
    # Define la plantilla que se utilizará para renderizar el formulario.
    template_name = 'comisariastolhuin/tolhuin/comisaria_tolhuin_form.html'
    
    # Define la URL a la que se redirigirá al usuario después de crear el objeto.
    success_url = reverse_lazy('comisaria_tolhuin_list')

    # Método que determina si el usuario tiene permiso para acceder a esta vista.
    def test_func(self):
        # Verifica si el usuario pertenece al grupo 'comisariatolhuin'.
        return user_is_in_group(self.request.user, 'comisariatolhuin')

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
        context['codigos_policialesTOL'] = CodigoPolicialTOL.objects.all()
        
        # Añade al contexto todos los objetos de DependenciasSecundariasTOL.
        context['dependencias_secundariasTOL'] = DependenciasSecundariasTOL.objects.all()

        # Inicializa detalles adicionales como listas vacías en el contexto para la vista de creación.
        context['detalle_servicios_emergenciaTOL'] = json.dumps([])
        context['detalle_instituciones_hospitalariasTOL'] = json.dumps([])
        context['detalle_dependencias_municipalesTOL'] = json.dumps([])
        context['detalle_dependencias_provincialesTOL'] = json.dumps([])
        context['detalle_dependencias_secundariasTOL'] = json.dumps([])
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
            for servicioTOL in form.cleaned_data['servicios_emergenciaTOL']:
                # Obtiene los datos específicos para cada servicio de emergencia desde el formulario.
                numero_movil_bomberosTOL = self.request.POST.get(f'numero_movil_bomberos_{servicioTOL.id}')
                nombre_a_cargo_bomberosTOL = self.request.POST.get(f'nombre_a_cargo_bomberos_{servicioTOL.id}')
                
                # Si se proporcionan datos, crea un registro en DetalleServicioEmergencia.
                if numero_movil_bomberosTOL or nombre_a_cargo_bomberosTOL:
                    DetalleServicioEmergenciaTOL.objects.create(
                        servicio_emergenciaTOL=servicioTOL,
                        comisaria_tolhuin=self.object,
                        numero_movil_bomberosTOL=numero_movil_bomberosTOL,
                        nombre_a_cargo_bomberosTOL=nombre_a_cargo_bomberosTOL
                    )

            # Guardar los detalles adicionales para cada institución hospitalaria.
            for institucionTOL in form.cleaned_data['instituciones_hospitalariasTOL']:
                # Obtiene los datos específicos para cada institución hospitalaria desde el formulario.
                numero_movil_hospitalTOL = self.request.POST.get(f'numero_movil_hospital_{institucionTOL.id}')
                nombre_a_cargo_hospitalTOL = self.request.POST.get(f'nombre_a_cargo_hospital_{institucionTOL.id}')
                
                # Si se proporcionan datos, crea un registro en DetalleInstitucionHospitalaria.
                if numero_movil_hospitalTOL or nombre_a_cargo_hospitalTOL:
                    DetalleInstitucionHospitalariaTOL.objects.create(
                        institucion_hospitalariaTOL=institucionTOL,
                        comisaria_tolhuin=self.object,
                        numero_movil_hospitalTOL=numero_movil_hospitalTOL,
                        nombre_a_cargo_hospitalTOL=nombre_a_cargo_hospitalTOL
                    )

            # Guardar los detalles adicionales para cada dependencia municipal.
            for dependencia_municipalTOL in form.cleaned_data['dependencias_municipalesTOL']:
                # Obtiene los datos específicos para cada dependencia municipal desde el formulario.
                numero_movil_municipalTOL = self.request.POST.get(f'numero_movil_municipal_{dependencia_municipalTOL.id}')
                nombre_a_cargo_municipalTOL = self.request.POST.get(f'nombre_a_cargo_municipal_{dependencia_municipalTOL.id}')
                
                # Si se proporcionan datos, crea un registro en DetalleDependenciaMunicipal.
                if numero_movil_municipalTOL or nombre_a_cargo_municipalTOL:
                    DetalleDependenciaMunicipalTOL.objects.create(
                        dependencia_municipalTOL=dependencia_municipalTOL,
                        comisaria_tolhuin=self.object,
                        numero_movil_municipalTOL=numero_movil_municipalTOL,
                        nombre_a_cargo_municipalTOL=nombre_a_cargo_municipalTOL
                    )

            # Guardar los detalles adicionales para cada dependencia provincial.
            for dependencia_provincialTOL in form.cleaned_data['dependencias_provincialesTOL']:
                # Obtiene los datos específicos para cada dependencia provincial desde el formulario.
                numero_movil_provincialTOL = self.request.POST.get(f'numero_movil_provincial_{dependencia_provincialTOL.id}')
                nombre_a_cargo_provincialTOL = self.request.POST.get(f'nombre_a_cargo_provincial_{dependencia_provincialTOL.id}')
                
                # Si se proporcionan datos, crea un registro en DetalleDependenciaProvincial.
                if numero_movil_provincialTOL or nombre_a_cargo_provincialTOL:
                    DetalleDependenciaProvincialTOL.objects.create(
                        dependencia_provincialTOL=dependencia_provincialTOL,
                        comisaria_tolhuin=self.object,
                        numero_movil_provincialTOL=numero_movil_provincialTOL,
                        nombre_a_cargo_provincialTOL=nombre_a_cargo_provincialTOL
                    )

            # Guardar los detalles adicionales para dependencias secundarias
            for dependencia_secundariaTOL in form.cleaned_data['dependencias_secundariasTOL']:
                numero_movil_secundariaTOL = self.request.POST.get(f'numero_movil_secundaria_{dependencia_secundariaTOL.id}')
                nombre_a_cargo_secundariaTOL = self.request.POST.get(f'nombre_a_cargo_secundaria_{dependencia_secundariaTOL.id}')
                if numero_movil_secundariaTOL or nombre_a_cargo_secundariaTOL:
                    DetalleDependenciaSecundariaTOL.objects.create(
                        dependencia_secundariaTOL=dependencia_secundariaTOL,
                        comisaria_tolhuin=self.object,
                        numero_movil_secundariaTOL=numero_movil_secundariaTOL,
                        nombre_a_cargo_secundariaTOL=nombre_a_cargo_secundariaTOL
                    )

            # Guardar los detalles adicionales para instituciones federales
            for institucion_federal in form.cleaned_data['instituciones_federales']:
                numero_movil_federal = self.request.POST.get(f'numero_movil_federal_{institucion_federal.id}')
                nombre_a_cargo_federal = self.request.POST.get(f'nombre_a_cargo_federal_{institucion_federal.id}')
                if numero_movil_federal or nombre_a_cargo_federal:
                    DetalleInstitucionFederal.objects.create(
                        institucion_federal=institucion_federal,
                        comisaria_tolhuin=self.object,
                        numero_movil_federal=numero_movil_federal,
                        nombre_a_cargo_federal=nombre_a_cargo_federal
                    )        

            # Llama al método form_valid de la clase base para completar la operación.
            # Añadir un mensaje de éxito al sistema de mensajes
            messages.success(self.request, 'El código ha sido guardado exitosamente.')
            
            return super().form_valid(form)
        
    
     #------------------------clase para el edit updtae------------------------------------------------------


class ComisariaTolhuinUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # Especifica el modelo de datos que se va a actualizar.
    model = ComisariaTolhuin
    
    # Especifica el formulario que se utilizará para actualizar el objeto.
    form_class = ComisariaTolhuinForm
    
    # Define la plantilla que se utilizará para renderizar el formulario.
    template_name = 'comisariastolhuin/tolhuin/comisaria_tolhuin_form.html'
    
    # Define la URL a la que se redirigirá al usuario después de actualizar el objeto.
    success_url = reverse_lazy('comisaria_tolhuin_list')

    # Método que determina si el usuario tiene permiso para acceder a esta vista.
    def test_func(self):
        # Verifica si el usuario pertenece al grupo 'comisariatolhuin'.
        return user_is_in_group(self.request.user, 'comisariatolhuin')

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
            return redirect('comisaria_tolhuin_list')

        # Si no se cumplen las condiciones anteriores, sigue con el proceso normal.
        return super().dispatch(request, *args, **kwargs)

    # Método que proporciona datos adicionales al contexto de la plantilla.
    def get_context_data(self, **kwargs):
        # Llama al método original para obtener el contexto predeterminado.
        context = super().get_context_data(**kwargs)
        
        # Añade al contexto todos los objetos de CodigoPolicialUSH.
        context['codigos_policialesTOL'] = CodigoPolicialTOL.objects.all()
        
        # Añade al contexto todos los objetos de DependenciasSecundarias.
        context['dependencias_secundariasTOL'] = DependenciasSecundariasTOL.objects.all()

        # Convierte los detalles en JSON para ser usados por Alpine.js
        context['detalle_servicios_emergenciaTOL'] = json.dumps(list(
            DetalleServicioEmergenciaTOL.objects.filter(comisaria_tolhuin=self.object.pk).values('id', 'servicio_emergenciaTOL_id', 'numero_movil_bomberosTOL', 'nombre_a_cargo_bomberosTOL')
        ))

        context['detalle_instituciones_hospitalariasTOL'] = json.dumps(list(
            DetalleInstitucionHospitalariaTOL.objects.filter(comisaria_tolhuin=self.object.pk).values('id', 'institucion_hospitalariaTOL_id', 'numero_movil_hospitalTOL', 'nombre_a_cargo_hospitalTOL')
        ))

        context['detalle_dependencias_municipalesTOL'] = json.dumps(list(
            DetalleDependenciaMunicipalTOL.objects.filter(comisaria_tolhuin=self.object.pk).values('id', 'dependencia_municipalTOL_id', 'numero_movil_municipalTOL', 'nombre_a_cargo_municipalTOL')
        ))

        context['detalle_dependencias_provincialesTOL'] = json.dumps(list(
            DetalleDependenciaProvincialTOL.objects.filter(comisaria_tolhuin=self.object.pk).values('id', 'dependencia_provincialTOL_id', 'numero_movil_provincialTOL', 'nombre_a_cargo_provincialTOL')
        ))

         # Añadir los nuevos detalles para dependencias secundarias
        context['detalle_dependencias_secundariasTOL'] = json.dumps(list(
            DetalleDependenciaSecundariaTOL.objects.filter(comisaria_tolhuin=self.object.pk).values('id', 'dependencia_secundariaTOL_id', 'numero_movil_secundariaTOL', 'nombre_a_cargo_secundariaTOL')
        ))

        # Añadir los nuevos detalles para instituciones federales
        context['detalle_instituciones_federales'] = json.dumps(list(
            DetalleInstitucionFederal.objects.filter(comisaria_tolhuin=self.object.pk).values('id', 'institucion_federal_id', 'numero_movil_federal', 'nombre_a_cargo_federal')
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
        servicios_emergencia_ids = form.cleaned_data['servicios_emergenciaTOL'].values_list('id', flat=True)
        instituciones_hospitalarias_ids = form.cleaned_data['instituciones_hospitalariasTOL'].values_list('id', flat=True)
        dependencias_municipales_ids = form.cleaned_data['dependencias_municipalesTOL'].values_list('id', flat=True)
        dependencias_provinciales_ids = form.cleaned_data['dependencias_provincialesTOL'].values_list('id', flat=True)
        dependencias_secundarias_ids = form.cleaned_data['dependencias_secundariasTOL'].values_list('id', flat=True)
        instituciones_federales_ids = form.cleaned_data['instituciones_federales'].values_list('id', flat=True)


        # Eliminar los detalles que ya no están seleccionados.
        DetalleServicioEmergenciaTOL.objects.filter(comisaria_tolhuin=self.object).exclude(servicio_emergenciaTOL_id__in=servicios_emergencia_ids).delete()
        DetalleInstitucionHospitalariaTOL.objects.filter(comisaria_tolhuin=self.object).exclude(institucion_hospitalariaTOL_id__in=instituciones_hospitalarias_ids).delete()
        DetalleDependenciaMunicipalTOL.objects.filter(comisaria_tolhuin=self.object).exclude(dependencia_municipalTOL_id__in=dependencias_municipales_ids).delete()
        DetalleDependenciaProvincialTOL.objects.filter(comisaria_tolhuin=self.object).exclude(dependencia_provincialTOL_id__in=dependencias_provinciales_ids).delete()
        DetalleDependenciaSecundariaTOL.objects.filter(comisaria_tolhuin=self.object).exclude(dependencia_secundariaTOL_id__in=dependencias_secundarias_ids).delete()
        DetalleInstitucionFederal.objects.filter(comisaria_tolhuin=self.object).exclude(institucion_federal_id__in=instituciones_federales_ids).delete()


        # Guardar los detalles adicionales para cada servicio de emergencia.
        for servicioTOL in form.cleaned_data['servicios_emergenciaTOL']:
            numero_movil_bomberosTOL = self.request.POST.get(f'numero_movil_bomberos_{servicioTOL.id}')
            nombre_a_cargo_bomberosTOL = self.request.POST.get(f'nombre_a_cargo_bomberos_{servicioTOL.id}')
            DetalleServicioEmergenciaTOL.objects.update_or_create(
                servicio_emergenciaTOL=servicioTOL,
                comisaria_tolhuin=self.object,
                defaults={
                    'numero_movil_bomberosTOL': numero_movil_bomberosTOL,
                    'nombre_a_cargo_bomberosTOL': nombre_a_cargo_bomberosTOL
                }
            )

        # Guardar los detalles adicionales para cada institución hospitalaria.
        for institucionTOL in form.cleaned_data['instituciones_hospitalariasTOL']:
            numero_movil_hospitalTOL = self.request.POST.get(f'numero_movil_hospital_{institucionTOL.id}')
            nombre_a_cargo_hospitalTOL= self.request.POST.get(f'nombre_a_cargo_hospital_{institucionTOL.id}')
            DetalleInstitucionHospitalariaTOL.objects.update_or_create(
                institucion_hospitalariaTOL=institucionTOL,
                comisaria_tolhuin=self.object,
                defaults={
                    'numero_movil_hospitalTOL': numero_movil_hospitalTOL,
                    'nombre_a_cargo_hospitalTOL': nombre_a_cargo_hospitalTOL
                }
            )

        # Guardar los detalles adicionales para cada dependencia municipal.
        for dependencia_municipalTOL in form.cleaned_data['dependencias_municipalesTOL']:
            numero_movil_municipalTOL = self.request.POST.get(f'numero_movil_municipal_{dependencia_municipalTOL.id}')
            nombre_a_cargo_municipalTOL = self.request.POST.get(f'nombre_a_cargo_municipal_{dependencia_municipalTOL.id}')
            DetalleDependenciaMunicipalTOL.objects.update_or_create(
                dependencia_municipalTOL=dependencia_municipalTOL,
                comisaria_tolhuin=self.object,
                defaults={
                    'numero_movil_municipalTOL': numero_movil_municipalTOL,
                    'nombre_a_cargo_municipalTOL': nombre_a_cargo_municipalTOL
                }
            )

        # Guardar los detalles adicionales para cada dependencia provincial.
        for dependencia_provincialTOL in form.cleaned_data['dependencias_provincialesTOL']:
            numero_movil_provincialTOL = self.request.POST.get(f'numero_movil_provincial_{dependencia_provincialTOL.id}')
            nombre_a_cargo_provincialTOL = self.request.POST.get(f'nombre_a_cargo_provincial_{dependencia_provincialTOL.id}')
            DetalleDependenciaProvincialTOL.objects.update_or_create(
                dependencia_provincialTOL=dependencia_provincialTOL,
                comisaria_tolhuin=self.object,
                defaults={
                    'numero_movil_provincialTOL': numero_movil_provincialTOL,
                    'nombre_a_cargo_provincialTOL': nombre_a_cargo_provincialTOL
                }
            )

          # Guardar detalles adicionales para cada dependencia secundaria
        for dependencia_secundariaTOL in form.cleaned_data['dependencias_secundariasTOL']:
            numero_movil_secundariaTOL = self.request.POST.get(f'numero_movil_secundaria_{dependencia_secundariaTOL.id}')
            nombre_a_cargo_secundariaTOL = self.request.POST.get(f'nombre_a_cargo_secundaria_{dependencia_secundariaTOL.id}')
            DetalleDependenciaSecundariaTOL.objects.update_or_create(
                dependencia_secundariaTOL=dependencia_secundariaTOL,
                comisaria_tolhuin=self.object,
                defaults={
                    'numero_movil_secundariaTOL': numero_movil_secundariaTOL,
                    'nombre_a_cargo_secundariaTOL': nombre_a_cargo_secundariaTOL
                }
            )

        # Guardar detalles adicionales para instituciones federales
        for institucion_federal in form.cleaned_data['instituciones_federales']:
            numero_movil_federal = self.request.POST.get(f'numero_movil_federal_{institucion_federal.id}')
            nombre_a_cargo_federal = self.request.POST.get(f'nombre_a_cargo_federal_{institucion_federal.id}')
            DetalleInstitucionFederal.objects.update_or_create(
                institucion_federal=institucion_federal,
                comisaria_tolhuin=self.object,
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



class ComisariaTolhuinDetailView(DetailView):
    model = ComisariaTolhuin
    template_name = 'comisariastolhuin/tolhuin/comisaria_tolhuin_detail.html'
    context_object_name = 'record'




#----------------------------softdelete-------------------------------------------------------------

# En views.py

def eliminar_comisaria_tolhuin(request, pk):
    # Obtén el registro a eliminar
    comisaria = get_object_or_404(ComisariaTolhuin, pk=pk)
    
    # Marca el registro como inactivo
    comisaria.activo = False
    comisaria.save()
    
    # Envía un mensaje de confirmación
    messages.success(request, 'El código ha sido eliminado correctamente.')
    
    # Redirige de vuelta a la lista
    return redirect('comisaria_tolhuin_list')




#---------------------------------------------------------------------------------------------------------------------------------------

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
    template = get_template('comisariastolhuin/comisariaTOL_pdf_template.html')

    
    # Convierte la imagen a base64
    escudo_path = os.path.join(settings.BASE_DIR, 'comisariastolhuin', 'static', 'comisariastolhuin', 'images', 'ESCUDO POLICIA.jpeg')
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


def generate_comisaria_tolhuin_pdf_view(request):
    # Llama a la función view_pdf_content, pasando el request y el modelo ComisariaTolhuin.
    # Esta función generará el contenido del PDF para la ComisariaTolhuin y lo devolverá como una respuesta HTTP.
    return view_pdf_content(request, ComisariaTolhuin)

def generate_comisaria_tolhuin_pdf_download(request):
    add_signature = 'signature' in request.GET
    now = datetime.now()

  # Guarda el verbose_name original
    original_verbose_name = ComisariaTolhuin._meta.verbose_name
    
    # Redefine verbose_name temporalmente
    ComisariaTolhuin._meta.verbose_name = "Comisaría Tolhuin"

    # Define el nombre del archivo.
    filename = f"libro-diario-Comisaría-Tolhuin-{now.strftime('%d-%m-%Y')}.pdf"
    
    # Llama a generate_pdf
    response = generate_pdf(request, ComisariaTolhuin, filename, add_signature=add_signature)

    # Restaura el verbose_name original
    ComisariaTolhuin._meta.verbose_name = original_verbose_name

    return response


#------------------------------Descargar PDF del día anterior para Comisaria Tolhuin----------------------------------------



def generate_comisaria_tolhuin_pdf_download_previous_day(request):
    # Verifica si la URL contiene el parámetro 'signature' en la cadena de consulta (GET).
    add_signature = 'signature' in request.GET
    
    # Obtiene la fecha y hora actual.
    now = datetime.now()

    # Define el nombre de la comisaría sin "TOL".
    comisaria_name = "Comisaría Tolhuin"

    # Calcula la fecha del día anterior.
    previous_day = now - timedelta(days=1)
    
    # Define el nombre del archivo para el PDF, incluyendo "libro-diario", 
    # la fecha del día anterior, y la extensión ".pdf".
    filename = f"libro-diario-{comisaria_name}-{previous_day.strftime('%d-%m-%Y')}.pdf"
    
    # Genera el PDF para la fecha específica y lo devuelve como una respuesta HTTP.
    return generate_pdf_for_specific_date(request, ComisariaTolhuin, previous_day, filename, add_signature=add_signature)  


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
    template = get_template('comisariastolhuin/comisariaTOL_pdf_template.html')
    
    # Convierte la imagen a base64
    escudo_path = os.path.join(settings.BASE_DIR, 'comisariastolhuin', 'static', 'comisariastolhuin', 'images', 'ESCUDO POLICIA.jpeg')
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

def subir_pdfTOL(request):
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
                folder = 'partespdfTOL/'
                fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, folder))
                filename = fs.save(pdf.name, pdf)
                new_pdf = UploadedPDFTOL(file=os.path.join(folder, filename), uploaded_by=request.user)
                new_pdf.save()
                return JsonResponse({'success': 'El archivo PDF se ha subido correctamente.'})
            except Exception as e:
                return JsonResponse({'error': f'Error al subir el archivo: {str(e)}'})
        else:
            return JsonResponse({'error': 'No se seleccionó ningún archivo.'})
    return render(request, 'comisariastolhuin/subir_pdfTOL.html')


#-----------------------------------funcion para ver todos los registros  de los pdfTOL--------------------------------------------------------------



from django.http import FileResponse

def ver_pdfsTOL(request):
    # Obtiene todos los registros de PDF almacenados en la base de datos
    pdfs = UploadedPDFTOL.objects.all()
    
    # Renderiza la plantilla 'ver_pdfsTOL.html' y pasa los registros de PDF al contexto
    return render(request, 'comisariastolhuin/ver_pdfsTOL.html', {'pdfs': pdfs})

def mostrar_pdfTOL(request, pdf_id):
    # Obtiene el objeto UploadedPDFDTOL por ID
    pdf = UploadedPDFTOL.objects.get(id=pdf_id)
    
    # Abre el archivo desde el sistema de archivos
    pdf_path = pdf.file.path
    response = FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')
    
    # Asegúrate de que el PDF se abra en el navegador en lugar de descargarse
    response['Content-Disposition'] = 'inline; filename="%s"' % pdf.file.name
    
    return response


#-----------------------aqui empieza las funciones de comisarias tolhuin----------------------------------------------------


# Repite las siguientes funciones para las demás comisarías...
def generate_comisaria_tolhuin_pdf_view(request):
    return view_pdf_content(request, ComisariaTolhuin)

def generate_comisaria_tolhuin_pdf_download(request):
    add_signature = 'signature' in request.GET
    now = datetime.now()

  # Guarda el verbose_name original
    original_verbose_name = ComisariaTolhuin._meta.verbose_name
    
    # Redefine verbose_name temporalmente
    ComisariaTolhuin._meta.verbose_name = "Comisaría Tolhuin"

    # Define el nombre del archivo.
    filename = f"libro-diario-Comisaría-Tolhuin-{now.strftime('%d-%m-%Y')}.pdf"
    
    # Llama a generate_pdf
    response = generate_pdf(request, ComisariaTolhuin, filename, add_signature=add_signature)

    # Restaura el verbose_name original
    ComisariaTolhuin._meta.verbose_name = original_verbose_name

    return response


#------------------------------Descargar PDF del día anterior para Comisaria TolhuinTOL----------------------------------------



def generate_comisaria_tolhuin_pdf_download_previous_day(request):
    # Verifica si la URL contiene el parámetro 'signature' en la cadena de consulta (GET).
    add_signature = 'signature' in request.GET
    
    # Obtiene la fecha y hora actual.
    now = datetime.now()

    # Define el nombre de la comisaría sin "TOL".
    comisaria_name = "Comisaría Tolhuin"

    # Calcula la fecha del día anterior.
    previous_day = now - timedelta(days=1)
    
    # Define el nombre del archivo para el PDF, incluyendo "libro-diario", 
    # la fecha del día anterior, y la extensión ".pdf".
    filename = f"libro-diario-{comisaria_name}-{previous_day.strftime('%d-%m-%Y')}.pdf"
    
    # Genera el PDF para la fecha específica y lo devuelve como una respuesta HTTP.
    return generate_pdf_for_specific_date(request, ComisariaTolhuin, previous_day, filename, add_signature=add_signature)  





#--------------------FUNCION PARA GENERAR PDFS PARA FECHAS ESPECIFICAS---------------------#

def generate_pdf_for_date_and_range(request, comisaria_model, start_time, end_time, filename, add_signature=False):
    """
    Genera un PDF basado en un rango de fechas y horas especificado.

    :param request: Solicitud HTTP de Django.
    :param comisaria_model: Modelo de la base de datos a filtrar.
    :param start_time: Fecha y hora de inicio del rango.
    :param end_time: Fecha y hora de fin del rango.
    :param filename: Nombre del archivo PDF.
    :param add_signature: Booleano para indicar si se agrega firma.
    """
    # Filtrar los registros en el rango horario
    registros = comisaria_model.objects.filter(
        models.Q(created_at__range=(start_time, end_time)) |
        models.Q(updated_at__range=(start_time, end_time)),
        activo=True  # Filtrar solo registros activos
    )

    # Cargar la plantilla HTML
    template = get_template('comisariastolhuin/comisariaTOL_pdf_template.html')

    # Convertir la imagen a base64
    escudo_path = os.path.join(settings.BASE_DIR, 'comisariastolhuin', 'static', 'comisariastolhuin', 'images', 'ESCUDO POLICIA.jpeg')
    with open(escudo_path, "rb") as img_file:
        escudo_base64 = base64.b64encode(img_file.read()).decode('utf-8')

    # Preparar el contexto para la plantilla
    context = {
        'registros': registros,
        'comisaria_name': comisaria_model._meta.verbose_name.title(),
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


def generate_pdf_custom_range_view(request):
    # Obtener los valores del formulario
    start_date = request.GET.get('start_date')  # Formato: 'YYYY-MM-DD'
    start_time = request.GET.get('start_time')  # Formato: 'HH:MM'
    end_date = request.GET.get('end_date')      # Formato: 'YYYY-MM-DD'
    end_time = request.GET.get('end_time')      # Formato: 'HH:MM'

    # Combinar fecha y hora en objetos datetime
    try:
        start_datetime = datetime.strptime(f"{start_date} {start_time}", '%Y-%m-%d %H:%M')
        end_datetime = datetime.strptime(f"{end_date} {end_time}", '%Y-%m-%d %H:%M')
    except (ValueError, TypeError):
        return HttpResponse('Error en el formato de fecha/hora', status=400)

    # Usar start_datetime y end_datetime como siempre
    filename = f"reporte-{start_datetime.strftime('%Y-%m-%d_%H-%M')}_to_{end_datetime.strftime('%Y-%m-%d_%H-%M')}.pdf"
    return generate_pdf_for_date_and_range(request, ComisariaTolhuin, start_datetime, end_datetime, filename)

#----------FUNCION PARA RENDERIZAR LA VISTA----------
def select_range_view_tol(request):
    # Renderizar el formulario para seleccionar el rango
    return render(request, 'comisariastolhuin/select_range_tolhuin.html')
