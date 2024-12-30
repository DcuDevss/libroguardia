from Libropolicial.forms import CustomLoginForm
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import (
    ComisariaTolhuin, CodigoPolicialTOL, 
    CodigosSecundariosTOL, DependenciasSecundariasTOL, CuartoGuardiaTOL, InstitucionesFederales,
    InstitucionesHospitalariasTOL, DependenciasMunicipalesTOL, DependenciasProvincialesTOL,
    ServiciosEmergenciaTOL, DetalleServicioEmergenciaTOL, DetalleInstitucionHospitalariaTOL,
    DetalleDependenciaMunicipalTOL, DetalleDependenciaProvincialTOL, DetalleDependenciaSecundariaTOL, DetalleInstitucionFederal, SolicitanteCodigoTOL
)

# Formulario para DetalleDependenciaSecundaria
class DetalleDependenciaSecundariaTOLForm(forms.ModelForm):
    dependencia_secundariaTOL = forms.ModelChoiceField(
        queryset=DependenciasSecundariasTOL.objects.filter(activo=True),  # Solo dependencias secundarias activas
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = DetalleDependenciaSecundariaTOL
        fields = ['dependencia_secundariaTOL', 'numero_movil_secundariaTOL', 'nombre_a_cargo_secundariaTOL']
        widgets = {
            'numero_movil_secundariaTOL': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
            'nombre_a_cargo_secundariaTOL': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
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

# Formulario para DetalleServicioEmergencia
class DetalleServicioEmergenciaTOLForm(forms.ModelForm):
    servicio_emergenciaTOL = forms.ModelChoiceField(
        queryset=ServiciosEmergenciaTOL.objects.filter(activo=True),  # Solo servicios de emergencia activos
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = DetalleServicioEmergenciaTOL
        fields = ['servicio_emergenciaTOL', 'numero_movil_bomberosTOL', 'nombre_a_cargo_bomberosTOL']
        widgets = {
            'numero_movil_bomberosTOL': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
            'nombre_a_cargo_bomberosTOL': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
        }

# Formulario para DetalleInstitucionHospitalaria
class DetalleInstitucionHospitalariaTOLForm(forms.ModelForm):
    institucion_hospitalariaTOL = forms.ModelChoiceField(
        queryset=InstitucionesHospitalariasTOL.objects.filter(activo=True),  # Solo instituciones hospitalarias activas
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = DetalleInstitucionHospitalariaTOL
        fields = ['institucion_hospitalariaTOL', 'numero_movil_hospitalTOL', 'nombre_a_cargo_hospitalTOL']
        widgets = {
            'numero_movil_hospitalTOL': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
            'nombre_a_cargo_hospitalTOL': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
        }

# Formulario para DetalleDependenciaMunicipal
class DetalleDependenciaMunicipalTOLForm(forms.ModelForm):
    dependencia_municipalTOL = forms.ModelChoiceField(
        queryset=DependenciasMunicipalesTOL.objects.filter(activo=True),  # Solo dependencias municipales activas
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = DetalleDependenciaMunicipalTOL
        fields = ['dependencia_municipalTOL', 'numero_movil_municipalTOL', 'nombre_a_cargo_municipalTOL']
        widgets = {
            'numero_movil_municipalTOL': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
            'nombre_a_cargo_municipalTOL': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
        }

# Formulario para DetalleDependenciaProvincial
class DetalleDependenciaProvincialTOLForm(forms.ModelForm):
    dependencia_provincialTOL = forms.ModelChoiceField(
        queryset=DependenciasProvincialesTOL.objects.filter(activo=True),  # Solo dependencias provinciales activas
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = DetalleDependenciaProvincialTOL
        fields = ['dependencia_provincialTOL', 'numero_movil_provincialTOL', 'nombre_a_cargo_provincialTOL']
        widgets = {
            'numero_movil_provincialTOL': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
            'nombre_a_cargo_provincialTOL': forms.TextInput(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'}),
        }

# Otros formularios de BaseComisariaForm y las comisarías ya estarían bien con el resto del código que has proporcionado.



class BaseComisariaTOLForm(forms.ModelForm):
    # Campo para seleccionar el cuarto de guardia
    cuartoTOL = forms.ModelChoiceField(
        queryset=CuartoGuardiaTOL.objects.filter(activo=True),  # Solo cuartos activos
        required=False,
        label='Cuarto',
        widget=forms.Select(attrs={'class': 'cursor-pointer bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3 appearance-none'})
    )


    # Campo para seleccionar el solicitante de código
    solicitante_codigoTOL = forms.ModelChoiceField(
        queryset=SolicitanteCodigoTOL.objects.filter(activo=True),  # Solo solicitantes activos
        required=False,
        label='Solicitante del Código',
        widget=forms.Select(attrs={'class': 'cursor-pointer bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3 appearance-none'})
    )

    # Campo para seleccionar el código policial principal
    codigoTOL = forms.ModelChoiceField(
        queryset=CodigoPolicialTOL.objects.filter(activo=True),  # Solo códigos activos
        required=False,
        label='Código Principal',
        widget=forms.Select(attrs={'class': 'cursor-pointer bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3 appearance-none'})
    )

    # Campo para seleccionar las dependencias secundarias
    dependencias_secundariasTOL = forms.ModelMultipleChoiceField(
        queryset=DependenciasSecundariasTOL.objects.filter(activo=True),  # Solo dependencias secundarias activas
        required=False,
        label='Dependencias Policiales',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'})
    )

    # Campo para seleccionar múltiples códigos secundarios
    codigos_secundariosTOL = forms.ModelMultipleChoiceField(
        queryset=CodigosSecundariosTOL.objects.filter(activo=True),  # Solo códigos secundarios activos
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
    instituciones_hospitalariasTOL = forms.ModelMultipleChoiceField(
        queryset=InstitucionesHospitalariasTOL.objects.filter(activo=True),  # Solo instituciones hospitalarias activas
        required=False,
        label='Instituciones Hospitalarias',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'})
    )

    # Campo para seleccionar múltiples dependencias municipales
    dependencias_municipalesTOL = forms.ModelMultipleChoiceField(
        queryset=DependenciasMunicipalesTOL.objects.filter(activo=True),  # Solo dependencias municipales activas
        required=False,
        label='Dependencias Municipales',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'})
    )

    # Campo para seleccionar múltiples dependencias provinciales
    dependencias_provincialesTOL = forms.ModelMultipleChoiceField(
        queryset=DependenciasProvincialesTOL.objects.filter(activo=True),  # Solo dependencias provinciales activas
        required=False,
        label='Dependencias Provinciales',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'})
    )

    # Campo para seleccionar múltiples servicios de emergencia
    servicios_emergenciaTOL = forms.ModelMultipleChoiceField(
        queryset=ServiciosEmergenciaTOL.objects.filter(activo=True),  # Solo servicios de emergencia activos
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
            'cuartoTOL', 'fecha_hora', 'codigoTOL', 'solicitante_codigoTOL', 'dependencias_secundariasTOL', 'codigos_secundariosTOL', 
            'movil_patrulla', 'a_cargo', 'secundante', 'lugar_codigo', 'descripcion', 
            'instituciones_intervinientes', 'tareas_judiciales', 'estado', 
            'instituciones_hospitalariasTOL', 'dependencias_municipalesTOL', 'dependencias_provincialesTOL', 'servicios_emergenciaTOL', 'instituciones_federales'
        ]
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'estado': forms.CheckboxInput(attrs={'class': 'sr-only peer'}),
        }

# Formulario específico para ComisariaTolhuin, basado en BaseComisariaForm
class ComisariaTolhuinForm(BaseComisariaTOLForm):
    class Meta(BaseComisariaTOLForm.Meta):
        model = ComisariaTolhuin



