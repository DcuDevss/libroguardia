from django.contrib import admin
from .models import (  
    DependenciasSecundariasTOL, SolicitanteCodigoTOL, ServiciosEmergenciaTOL, 
    InstitucionesHospitalariasTOL, DependenciasMunicipalesTOL, DependenciasProvincialesTOL,
   
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
@admin.register(DependenciasSecundariasTOL)
class DependenciasSecundariasTOLAdmin(admin.ModelAdmin):
    list_display = ('dependenciaTOL', 'activo')
    search_fields = ('dependenciaTOL',)
    list_filter = ('activo',)
    list_per_page = 20  # Paginación
    actions = [make_active, make_inactive]  # Acciones personalizadas

# Admin para SolicitanteCodigo con opciones de activar/desactivar y paginación
@admin.register(SolicitanteCodigoTOL)
class SolicitanteCodigoTOLAdmin(admin.ModelAdmin):
    list_display = ('codigoTOL', 'activo')
    search_fields = ('codigoTOL',)
    list_filter = ('activo',)
    list_per_page = 20  # Paginación
    actions = [make_active, make_inactive]  # Acciones personalizadas

# Admin para ServiciosEmergencia con opciones de activar/desactivar y paginación
@admin.register(ServiciosEmergenciaTOL)
class ServiciosEmergenciaTOLAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    search_fields = ('nombre',)
    list_filter = ('activo',)
    list_per_page = 20  # Paginación
    actions = [make_active, make_inactive]  # Acciones personalizadas

# Admin para InstitucionesHospitalarias con opciones de activar/desactivar y paginación
@admin.register(InstitucionesHospitalariasTOL)
class InstitucionesHospitalariasTOLAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    search_fields = ('nombre',)
    list_filter = ('activo',)
    list_per_page = 20  # Paginación
    actions = [make_active, make_inactive]  # Acciones personalizadas

# Admin para DependenciasMunicipales con opciones de activar/desactivar y paginación
@admin.register(DependenciasMunicipalesTOL)
class DependenciasMunicipalesTOLAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    search_fields = ('nombre',)
    list_filter = ('activo',)
    list_per_page = 20  # Paginación
    actions = [make_active, make_inactive]  # Acciones personalizadas

# Admin para DependenciasProvinciales con opciones de activar/desactivar y paginación
@admin.register(DependenciasProvincialesTOL)
class DependenciasProvincialesTOLAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    search_fields = ('nombre',)
    list_filter = ('activo',)
    list_per_page = 20  # Paginación
    actions = [make_active, make_inactive]  # Acciones personalizadas

