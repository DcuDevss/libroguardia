from django.contrib import admin
from .models import (  
    DependenciasSecundarias, SolicitanteCodigo, ServiciosEmergencia, 
    InstitucionesHospitalarias, DependenciasMunicipales, DependenciasProvinciales
)

# Acción para activar registros
def make_active(modeladmin, request, queryset):
    queryset.update(activo=True)
make_active.short_description = "Activar seleccionados"

# Acción para desactivar registros
def make_inactive(modeladmin, request, queryset):
    queryset.update(activo=False)
make_inactive.short_description = "Desactivar seleccionados"

# Admin para DependenciasSecundarias con opciones de activar/desactivar y paginación
@admin.register(DependenciasSecundarias)
class DependenciasSecundariasAdmin(admin.ModelAdmin):
    list_display = ('dependencia', 'activo')
    search_fields = ('dependencia',)
    list_filter = ('activo',)
    list_per_page = 20  # Paginación
    actions = [make_active, make_inactive]  # Acciones personalizadas

# Admin para SolicitanteCodigo con opciones de activar/desactivar y paginación
@admin.register(SolicitanteCodigo)
class SolicitanteCodigoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'activo')
    search_fields = ('codigo',)
    list_filter = ('activo',)
    list_per_page = 20  # Paginación
    actions = [make_active, make_inactive]  # Acciones personalizadas

# Admin para ServiciosEmergencia con opciones de activar/desactivar y paginación
@admin.register(ServiciosEmergencia)
class ServiciosEmergenciaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    search_fields = ('nombre',)
    list_filter = ('activo',)
    list_per_page = 20  # Paginación
    actions = [make_active, make_inactive]  # Acciones personalizadas

# Admin para InstitucionesHospitalarias con opciones de activar/desactivar y paginación
@admin.register(InstitucionesHospitalarias)
class InstitucionesHospitalariasAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    search_fields = ('nombre',)
    list_filter = ('activo',)
    list_per_page = 20  # Paginación
    actions = [make_active, make_inactive]  # Acciones personalizadas

# Admin para DependenciasMunicipales con opciones de activar/desactivar y paginación
@admin.register(DependenciasMunicipales)
class DependenciasMunicipalesAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    search_fields = ('nombre',)
    list_filter = ('activo',)
    list_per_page = 20  # Paginación
    actions = [make_active, make_inactive]  # Acciones personalizadas

# Admin para DependenciasProvinciales con opciones de activar/desactivar y paginación
@admin.register(DependenciasProvinciales)
class DependenciasProvincialesAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    search_fields = ('nombre',)
    list_filter = ('activo',)
    list_per_page = 20  # Paginación
    actions = [make_active, make_inactive]  # Acciones personalizadas
