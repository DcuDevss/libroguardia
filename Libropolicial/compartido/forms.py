# compartido/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm, User
from .models import CargaDatosPermiso

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese usuario',
        'class': 'form-control rounded-md pl-1'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingrese contraseña',
        'class': 'contra form-control rounded-md pl-1'
    }))

class AsignarPermisoForm(forms.ModelForm):
    class Meta:
        model = CargaDatosPermiso
        fields = ['usuario', 'hora_inicio', 'hora_fin']

    # Personalización de widgets si quieres mostrar un formato amigable de hora
    hora_inicio = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    hora_fin = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    
    # Lista de usuarios disponibles para asignar permisos
    usuario = forms.ModelChoiceField(queryset=User.objects.all(), empty_label="Seleccione un usuario")