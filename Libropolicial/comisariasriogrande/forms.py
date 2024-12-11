# Libropolicial/comisariasriogrande/forms.py
from django import forms
from .models import ComisariaPrimeraRG, ComisariaSegundaRG, ComisariaTerceraRG, ComisariaCuartaRG, ComisariaQuintaRG
from Libropolicial.forms import CustomLoginForm  # Importar desde la ubicación comúnsubo nuevo

# Formularios para las comisarías
class BaseComisariaRGForm(forms.ModelForm):
    class Meta:
        fields = ['cuarto', 'codigo', 'movil_patrulla', 'a_cargo', 'secundante', 'nombre_victima', 'dni', 'sexo', 'estado_civil', 'domicilio', 'trabajo', 'descripcion']

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
