from django import forms
from django.forms import inlineformset_factory
from .models import DivisionComunicaciones, EventoGuardia, CuartoGuardiaUSH, EncargadoGuardia, PersonalGuardia, EventoGuardiaBis, EventoGuardiaBisUno


class DivisionComunicacionesForm(forms.ModelForm):
    encargado_guardia = forms.ModelChoiceField(
        queryset=EncargadoGuardia.objects.filter(activo=True),  # Solo muestra los encargados activos
        required=False,
        label="Encargado de Guardia",
        widget=forms.Select(
            attrs={
                'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'
            }
        )
    )

    personal_guardia = forms.ModelMultipleChoiceField(
        queryset=PersonalGuardia.objects.filter(activo=True),  # Solo muestra el personal activo
        required=False,
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'
            }
        ),
        label="Personal de Guardia"
    )

    cuarto = forms.ModelChoiceField(
        queryset=CuartoGuardiaUSH.objects.all(),
        required=False,
        label="Cuarto de Guardia",
        widget=forms.Select(
            attrs={
                'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'
            }
        )
    )

    inicio_guardia = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=False,
        label="Inicio de Guardia",
        input_formats=['%Y-%m-%dT%H:%M']
    )

    finalizacion_guardia = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=False,
        label="Finalización de Guardia",
        input_formats=['%Y-%m-%dT%H:%M']
    )

    oficial_servicio = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'
        }),
        label="Oficial de Servicio"
    )

    distribucion_personal_moviles = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'
        }),
        label="Distribución de Personal y Móviles"
    )

    novedades = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'bg-gray-50 dark:bg-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-3'
        }),
        label="Novedades"
    )

    class Meta:
        model = DivisionComunicaciones
        fields = [
            'encargado_guardia', 'personal_guardia', 'cuarto', 
            'inicio_guardia', 'finalizacion_guardia', 'oficial_servicio', 
            'distribucion_personal_moviles', 'novedades'
        ]







# Formulario para los eventos de tipo "Guardia Bis"
class EventoGuardiaBisForm(forms.ModelForm):
    class Meta:
        model = EventoGuardiaBis
        fields = ['tipo_eventobis', 'nombre_jerarquia']


# Formset para los eventos de tipo "Guardia Bis"
EventoGuardiaBisFormSet = inlineformset_factory(
    DivisionComunicaciones,
    EventoGuardiaBis,
    form=EventoGuardiaBisForm,
    extra=1,
    can_delete=True
)


# Formulario para los eventos de tipo "Guardia Bis Uno"
class EventoGuardiaBisUnoForm(forms.ModelForm):
    class Meta:
        model = EventoGuardiaBisUno
        fields = ['tipo_eventobisuno', 'movil_patrulla', 'nombre_jerarquia_movil_patrulla']


# Formset para los eventos de tipo "Guardia Bis Uno"
EventoGuardiaBisUnoFormSet = inlineformset_factory(
    DivisionComunicaciones,
    EventoGuardiaBisUno,
    form=EventoGuardiaBisUnoForm,
    extra=1,
    can_delete=True
)


# Formulario para los eventos de la guardia original
class EventoGuardiaForm(forms.ModelForm):
    hora_evento = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=True
    )

    class Meta:
        model = EventoGuardia
        fields = ['tipo_evento', 'hora_evento', 'descripcion']


# Formset para los eventos de la guardia original
EventoGuardiaFormSet = inlineformset_factory(
    DivisionComunicaciones,
    EventoGuardia,
    form=EventoGuardiaForm,
    fields=('tipo_evento', 'hora_evento', 'descripcion'),
    extra=1,
    can_delete=True
)
