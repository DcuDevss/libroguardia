import os    
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User  # Importa el modelo User de Django, que representa a los usuarios del sistema.
from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model
import random
from django.utils.timezone import now
from datetime import timedelta,datetime
from django.db import models
from django.contrib.auth import get_user_model
import random
from django.utils.timezone import now


# Create your models here.

class CuartoGuardiaUSH(models.Model):
    cuarto = models.CharField(max_length=1)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.cuarto

    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()

# Clase para manejar códigos policiales de Ushuaia.
class CodigoPolicialUSH(models.Model):
    codigo = models.CharField(max_length=10)  # Campo para almacenar un código, con un máximo de 10 caracteres.
    nombre_codigo = models.CharField(max_length=255, null=True, blank=True)  # Nuevo campo agregado que acepta nulos
    activo = models.BooleanField(default=True)  # Soft delete
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre_codigo}"  # Define la representación en cadena del objeto, mostrando el código.
    
    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()

# Clase para manejar códigos secundarios.
class CodigosSecundarios(models.Model):
    codigo = models.CharField(max_length=10)  # Campo para almacenar un código secundario, con un máximo de 10 caracteres.
    activo = models.BooleanField(default=True)  # Soft delete

    def __str__(self):
        return self.codigo  # Define la representación en cadena del objeto, mostrando el código.
    
    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()        

# Clase para manejar los archivos PDF subidos.
class UploadedPDF(models.Model):
    file = models.FileField(upload_to='partespdf/')  # Campo para almacenar archivos PDF, que se guardan en la carpeta 'partespdf/'.
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona cada PDF con el usuario que lo subió; si el usuario se elimina, también se elimina el PDF.
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Almacena la fecha y hora en que se subió el PDF, asignada automáticamente al crear el objeto.

    # Método para obtener solo el nombre del archivo PDF.
    def filename(self):
        return self.file.name.split('/')[-1]  # Retorna solo el nombre del archivo, eliminando el camino de la ruta.

class CuartoGuardiaRG(models.Model):
    cuartoRG = models.CharField(max_length=1)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.cuartoRG

    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()

# Clase para manejar códigos policiales de Ushuaia.
class CodigoPolicialRG(models.Model):
    codigoRG = models.CharField(max_length=10)  # Campo para almacenar un código, con un máximo de 10 caracteres.
    nombre_codigo = models.CharField(max_length=255, null=True, blank=True)  # Nuevo campo agregado que acepta nulos
    activo = models.BooleanField(default=True)  # Soft delete
    
    def __str__(self):
        return f"{self.codigoRG} - {self.nombre_codigo}"  # Define la representación en cadena del objeto, mostrando el código.
    
    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()

# Clase para manejar códigos secundarios.
class CodigosSecundariosRG(models.Model):
    codigoRG = models.CharField(max_length=10)  # Campo para almacenar un código secundario, con un máximo de 10 caracteres.
    activo = models.BooleanField(default=True)  # Soft delete

    def __str__(self):
        return self.codigoRG  # Define la representación en cadena del objeto, mostrando el código.
    
    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()        

# Clase para manejar los archivos PDF subidos.
class UploadedPDFRG(models.Model):
    file = models.FileField(upload_to='partespdfRG/')  # Campo para almacenar archivos PDF, que se guardan en la carpeta 'partespdf/'.
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona cada PDF con el usuario que lo subió; si el usuario se elimina, también se elimina el PDF.
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Almacena la fecha y hora en que se subió el PDF, asignada automáticamente al crear el objeto.

    # Método para obtener solo el nombre del archivo PDF.
    def filename(self):
        return self.file.name.split('/')[-1]  # Retorna solo el nombre del archivo, eliminando el camino de la ruta.
    

class CuartoGuardiaTOL(models.Model):
    cuartoTOL = models.CharField(max_length=1, null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.cuartoTOL

    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()

# Clase para manejar códigos policiales de tolhuin.
class CodigoPolicialTOL(models.Model):
    codigoTOL = models.CharField(max_length=10, null=True, blank=True)  # Campo para almacenar un código, con un máximo de 10 caracteres.
    nombre_codigo = models.CharField(max_length=255, null=True, blank=True)  # Nuevo campo agregado que acepta nulos
    activo = models.BooleanField(default=True)  # Soft delete
    
    def __str__(self):
        return f"{self.codigoTOL} - {self.nombre_codigo}"  # Define la representación en cadena del objeto, mostrando el código.
    
    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()

# Clase para manejar códigos secundarios.
class CodigosSecundariosTOL(models.Model):
    codigoTOL = models.CharField(max_length=10, null=True, blank=True)  # Campo para almacenar un código secundario, con un máximo de 10 caracteres.
    activo = models.BooleanField(default=True)  # Soft delete

    def __str__(self):
        return self.codigoTOL  # Define la representación en cadena del objeto, mostrando el código.
    
    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()        

# Clase para manejar los archivos PDF subidos.
class UploadedPDFTOL(models.Model):
    file = models.FileField(upload_to='partespdfTOL/')  # Campo para almacenar archivos PDF, que se guardan en la carpeta 'partespdf/'.
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona cada PDF con el usuario que lo subió; si el usuario se elimina, también se elimina el PDF.
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Almacena la fecha y hora en que se subió el PDF, asignada automáticamente al crear el objeto.

    # Método para obtener solo el nombre del archivo PDF.
    def filename(self):
        return self.file.name.split('/')[-1]  # Retorna solo el nombre del archivo, eliminando el camino de la ruta.    


def user_photo_path(instance, filename):
    """
    Genera una ruta única para almacenar la foto de perfil, usando el número de legajo.
    Si el legajo no está definido, usa el ID del usuario.
    """
    legajo = instance.legajo if instance.legajo else f"user_{instance.user.id}"
    extension = filename.split('.')[-1]  # Obtener la extensión del archivo
    return f'profiles/{legajo}/profile_image.{extension}'


from django.db import models
from django.conf import settings
import os

class Personal(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="personal_profile"
    )
    legajo = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="Legajo Personal")
    dni = models.CharField(max_length=15, unique=True, null=True, blank=True, verbose_name="DNI")
    telefono = models.CharField(max_length=15, null=True, blank=True, verbose_name="Teléfono")
    domicilio = models.CharField(max_length=100, null=True, blank=True, verbose_name="Domicilio")
    photo = models.ImageField(upload_to="profile_pictures/", null=True, blank=True, verbose_name="Foto de perfil")
    campos_completados = models.BooleanField(default=False, verbose_name="Campos completados")
    session_key = models.CharField(max_length=40, null=True, blank=True)  # Clave de sesión activa

    # Nuevos campos
    last_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="Última IP")
    last_device = models.CharField(max_length=255, null=True, blank=True, verbose_name="Último dispositivo")
    last_login_time = models.DateTimeField(null=True, blank=True, verbose_name="Última hora de conexión")
    is_online = models.BooleanField(default=False, verbose_name="Conectado")
    

    def save(self, *args, **kwargs):
        # Eliminar la foto anterior si se reemplaza
        if self.pk:
            old_instance = Personal.objects.filter(pk=self.pk).first()
            if old_instance and old_instance.photo and old_instance.photo != self.photo:
                if os.path.isfile(old_instance.photo.path):
                    os.remove(old_instance.photo.path)

        super().save(*args, **kwargs)

    def get_roles(self):
        """
        Devuelve una lista de nombres de grupos (roles) a los que pertenece el usuario.
        """
        return self.user.groups.values_list('name', flat=True)

    def get_permissions(self):
        """
        Devuelve una lista de nombres de permisos asociados directamente al usuario.
        """
        return self.user.user_permissions.values_list('name', flat=True)

    def __str__(self):
        return f"{self.user.username} - {self.legajo}"

User = get_user_model()

class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="otp")
    code = models.CharField(max_length=6)  # Código OTP de 6 dígitos
    created_at = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)  # Marca si el OTP sigue siendo válido

    def generate_code(self):
        # Verifica el número de OTP enviados en las últimas 24 horas
        recent_otp_count = OTP.objects.filter(
            user=self.user,
            created_at__gte=datetime.now() - timedelta(hours=24)
        ).count()

        if recent_otp_count >= 5:  # Límite de 5 OTP por día
            raise Exception("Se ha alcanzado el límite de solicitudes de OTP para hoy.")

        # Genera y guarda el nuevo código
        self.code = f"{random.randint(100000, 999999)}"
        self.is_valid = True
        self.created_at = now()
        self.save()

    def has_expired(self):
        expiration_time = timedelta(minutes=10)  # Define el tiempo de validez del OTP
        return now() > self.created_at + expiration_time

    def invalidate(self):
        self.is_valid = False
        self.save()