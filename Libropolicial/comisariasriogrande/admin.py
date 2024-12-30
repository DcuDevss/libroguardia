from django.contrib import admin
from .models import (  
    DependenciasSecundariasRG, SolicitanteCodigoRG, ServiciosEmergenciaRG, 
    InstitucionesHospitalariasRG, DependenciasMunicipalesRG, DependenciasProvincialesRG,
     ComisariaTerceraRG, ComisariaSegundaRG, ComisariaPrimeraRG,
    ComisariaCuartaRG, ComisariaQuintaRG
)

# Acción para activar registrosssok
def make_active(modeladmin, request, queryset):
    queryset.update(activo=True)
make_active.short_description = "Activar seleccionados"

# Acción para desactivar registros
def make_inactive(modeladmin, request, queryset):
    queryset.update(activo=False)
make_inactive.short_description = "Desactivar seleccionados"

# Admin para DependenciasSecundarias con opciones de activar/desactivar y paginación
@admin.register(DependenciasSecundariasRG)
class DependenciasSecundariasRGAdmin(admin.ModelAdmin):
    list_display = ('dependenciaRG', 'activo')
    search_fields = ('dependenciaRG',)
    list_filter = ('activo',)
    list_per_page = 20  # Paginación
    actions = [make_active, make_inactive]  # Acciones personalizadas

# Admin para SolicitanteCodigo con opciones de activar/desactivar y paginación
@admin.register(SolicitanteCodigoRG)
class SolicitanteCodigoRGAdmin(admin.ModelAdmin):
    list_display = ('codigoRG', 'activo')
    search_fields = ('codigoRG',)
    list_filter = ('activo',)
    list_per_page = 20  # Paginación
    actions = [make_active, make_inactive]  # Acciones personalizadas

# Admin para ServiciosEmergencia con opciones de activar/desactivar y paginación
@admin.register(ServiciosEmergenciaRG)
class ServiciosEmergenciaRGAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    search_fields = ('nombre',)
    list_filter = ('activo',)
    list_per_page = 20  # Paginación
    actions = [make_active, make_inactive]  # Acciones personalizadas

# Admin para InstitucionesHospitalarias con opciones de activar/desactivar y paginación
@admin.register(InstitucionesHospitalariasRG)
class InstitucionesHospitalariasRGAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    search_fields = ('nombre',)
    list_filter = ('activo',)
    list_per_page = 20  # Paginación
    actions = [make_active, make_inactive]  # Acciones personalizadas

# Admin para DependenciasMunicipales con opciones de activar/desactivar y paginación
@admin.register(DependenciasMunicipalesRG)
class DependenciasMunicipalesRGAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    search_fields = ('nombre',)
    list_filter = ('activo',)
    list_per_page = 20  # Paginación
    actions = [make_active, make_inactive]  # Acciones personalizadas

# Admin para DependenciasProvinciales con opciones de activar/desactivar y paginación
@admin.register(DependenciasProvincialesRG)
class DependenciasProvincialesRGAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    search_fields = ('nombre',)
    list_filter = ('activo',)
    list_per_page = 20  # Paginación
    actions = [make_active, make_inactive]  # Acciones personalizadas

