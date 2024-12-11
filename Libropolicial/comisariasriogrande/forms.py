# Libropolicial/comisariasriogrande/forms.py
from django import forms
from ckeditor.widgets import CKEditorWidget
from Libropolicial.forms import CustomLoginForm  # Importar desde la ubicación común
from .models import (ComisariaPrimeraRG, CodigoPolicialRG, ComisariaSegundaRG, ComisariaTerceraRG, ComisariaCuartaRG, ComisariaQuintaRG,CodigosSecundariosRG, DependenciasSecundariasRG, CuartoGuardiaRG, InstitucionesFederales,
InstitucionesHospitalariasRG, DependenciasMunicipalesRG, DependenciasProvincialesRG,
ServiciosEmergenciaRG, DetalleServicioEmergenciaRG, DetalleInstitucionHospitalariaRG,
DetalleDependenciaMunicipalRG, DetalleDependenciaProvincialRG, DetalleDependenciaSecundariaRG, DetalleInstitucionFederal, SolicitanteCodigoRG)


# Formulario para DetalleDependenciaSecundariaRG
class DetalleDependenciaSecundariaRGForm(forms.ModelForm):
    dependencia_secundariaRG = forms.ModelChoiceField(
        queryset=DependenciasSecundariasRG.objects.filter(activo=True),  # Solo dependencias secundarias activas
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = DetalleDependenciaSecundariaRG
        fields = ['dependencia_secundariaRG', 'numero_movil_secundariaRG', 'nombre_a_cargo_secundariaRG']
        widgets = {
            'numero_movil_secundariaRG': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
            'nombre_a_cargo_secundariaRG': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
        }

# Formulario para DetalleInstitucionFederal
class DetalleInstitucionFederalForm(forms.ModelForm):
    institucion_federal = forms.ModelChoiceField(
        queryset=InstitucionesFederales.objects.filter(activo=True),  # Solo instituciones federales activas
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = DetalleInstitucionFederal
        fields = ['institucion_federal', 'numero_movil_federal', 'nombre_a_cargo_federal']
        widgets = {
            'numero_movil_federal': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
            'nombre_a_cargo_federal': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
        }

# Formulario para DetalleServicioEmergenciaRG
class DetalleServicioEmergenciaRGForm(forms.ModelForm):
    servicio_emergenciaRG = forms.ModelChoiceField(
        queryset=ServiciosEmergenciaRG.objects.filter(activo=True),  # Solo servicios de emergencia activos
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = DetalleServicioEmergenciaRG
        fields = ['servicio_emergenciaRG', 'numero_movil_bomberosRG', 'nombre_a_cargo_bomberosRG']
        widgets = {
            'numero_movil_bomberosRG': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
            'nombre_a_cargo_bomberosRG': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
        }

# Formulario para DetalleInstitucionHospitalariaRG
class DetalleInstitucionHospitalariaRGForm(forms.ModelForm):
    institucion_hospitalariaRG = forms.ModelChoiceField(
        queryset=InstitucionesHospitalariasRG.objects.filter(activo=True),  # Solo instituciones hospitalarias activas
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = DetalleInstitucionHospitalariaRG
        fields = ['institucion_hospitalariaRG', 'numero_movil_hospitalRG', 'nombre_a_cargo_hospitalRG']
        widgets = {
            'numero_movil_hospitalRG': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
            'nombre_a_cargo_hospitalRG': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
        }

# Formulario para DetalleDependenciaMunicipalRG
class DetalleDependenciaMunicipalRGForm(forms.ModelForm):
    dependencia_municipalRG = forms.ModelChoiceField(
        queryset=DependenciasMunicipalesRG.objects.filter(activo=True),  # Solo dependencias municipales activas
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = DetalleDependenciaMunicipalRG
        fields = ['dependencia_municipalRG', 'numero_movil_municipalRG', 'nombre_a_cargo_municipalRG']
        widgets = {
            'numero_movil_municipalRG': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
            'nombre_a_cargo_municipalRG': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
        }

# Formulario para DetalleDependenciaProvincialRG
class DetalleDependenciaProvincialRGForm(forms.ModelForm):
    dependencia_provincialRG = forms.ModelChoiceField(
        queryset=DependenciasProvincialesRG.objects.filter(activo=True),  # Solo dependencias provinciales activas
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = DetalleDependenciaProvincialRG
        fields = ['dependencia_provincialRG', 'numero_movil_provincialRG', 'nombre_a_cargo_provincialRG']
        widgets = {
            'numero_movil_provincialRG': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
            'nombre_a_cargo_provincialRG': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
        }


# Formularios para las comisarías
class BaseComisariaRGForm(forms.ModelForm):
    # Campo para seleccionar el cuarto de guardia
    cuartoRG = forms.ModelChoiceField(
        queryset=CuartoGuardiaRG.objects.filter(activo=True),  # Solo cuartos activos
        required=False,
        label='Cuarto',
        widget=forms.Select(attrs={'class': 'cursor-pointer bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3 appearance-none'})
    )


    # Campo para seleccionar el solicitante de código
    solicitante_codigoRG = forms.ModelChoiceField(
        queryset=SolicitanteCodigoRG.objects.filter(activo=True),  # Solo solicitantes activos
        required=False,
        label='Solicitante del Código',
        widget=forms.Select(attrs={'class': 'cursor-pointer bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3 appearance-none'})
    )

    # Campo para seleccionar el código policial principal
    codigoRG = forms.ModelChoiceField(
        queryset=CodigoPolicialRG.objects.filter(activo=True),  # Solo códigos activos
        required=False,
        label='Código Principal',
        widget=forms.Select(attrs={'class': 'cursor-pointer bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3 appearance-none'})
    )

    # Campo para seleccionar las dependencias secundarias
    dependencias_secundariasRG = forms.ModelMultipleChoiceField(
        queryset=DependenciasSecundariasRG.objects.filter(activo=True),  # Solo dependencias secundarias activas
        required=False,
        label='Dependencias Policiales',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'})
    )

    # Campo para seleccionar múltiples códigos secundarios
    codigos_secundariosRG = forms.ModelMultipleChoiceField(
        queryset=CodigosSecundariosRG.objects.filter(activo=True),  # Solo códigos secundarios activos
        required=False,
        label='Códigos Secundarios',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'})
    )

    # Campo para seleccionar múltiples instituciones federales
    instituciones_federales = forms.ModelMultipleChoiceField(
        queryset=InstitucionesFederales.objects.filter(activo=True),  # Solo instituciones federales activas
        required=False,
        label='Instituciones Federales',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'})
    )

    # Campo para seleccionar múltiples instituciones hospitalarias
    instituciones_hospitalariasRG = forms.ModelMultipleChoiceField(
        queryset=InstitucionesHospitalariasRG.objects.filter(activo=True),  # Solo instituciones hospitalarias activas
        required=False,
        label='Instituciones Hospitalarias',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'})
    )

    # Campo para seleccionar múltiples dependencias municipales
    dependencias_municipalesRG = forms.ModelMultipleChoiceField(
        queryset=DependenciasMunicipalesRG.objects.filter(activo=True),  # Solo dependencias municipales activas
        required=False,
        label='Dependencias Municipales',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'})
    )

    # Campo para seleccionar múltiples dependencias provinciales
    dependencias_provincialesRG = forms.ModelMultipleChoiceField(
        queryset=DependenciasProvincialesRG.objects.filter(activo=True),  # Solo dependencias provinciales activas
        required=False,
        label='Dependencias Provinciales',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'})
    )

    # Campo para seleccionar múltiples servicios de emergencia
    servicios_emergenciaRG = forms.ModelMultipleChoiceField(
        queryset=ServiciosEmergenciaRG.objects.filter(activo=True),  # Solo servicios de emergencia activos
        required=False,
        label='Servicios de Emergencia Bomberil',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'})
    )

    # Campo de texto para la descripción
    descripcion = forms.CharField(
        widget=CKEditorWidget(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
        label='Descripción',
        required=False
    )

    class Meta:
        fields = [
            'cuartoRG', 'fecha_hora', 'codigoRG', 'solicitante_codigoRG', 'dependencias_secundariasRG', 'codigos_secundariosRG', 
            'movil_patrulla', 'a_cargo', 'secundante', 'lugar_codigo', 'descripcion', 
            'instituciones_intervinientes', 'tareas_judiciales', 'estado', 
            'instituciones_hospitalariasRG', 'dependencias_municipalesRG', 'dependencias_provincialesRG', 'servicios_emergenciaRG', 'instituciones_federales'
        ]
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'estado': forms.CheckboxInput(attrs={'class': 'sr-only peer'}),
        }

#Formulario para comisarias RG, basado en BaseComisariaRGForm
class ComisariaPrimeraRGForm(BaseComisariaRGForm):
    class Meta(BaseComisariaRGForm.Meta):
        model = ComisariaPrimeraRG

class ComisariaSegundaRGForm(BaseComisariaRGForm):
    class Meta(BaseComisariaRGForm.Meta):
        model = ComisariaSegundaRG

class ComisariaTerceraRGForm(BaseComisariaRGForm):
    class Meta(BaseComisariaRGForm.Meta):
        model = ComisariaTerceraRG

class ComisariaCuartaRGForm(BaseComisariaRGForm):
    class Meta(BaseComisariaRGForm.Meta):
        model = ComisariaCuartaRG

class ComisariaQuintaRGForm(BaseComisariaRGForm):
    class Meta(BaseComisariaRGForm.Meta):
        model = ComisariaQuintaRG
