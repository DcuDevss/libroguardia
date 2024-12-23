from django.db import models
from django.contrib.auth.models import User  # Importa el modelo User de Django, que representa a los usuarios del sistema.

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
    cuartoTOL = models.CharField(max_length=1)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.cuartoTOL

    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()

# Clase para manejar códigos policiales de Ushuaia.
class CodigoPolicialTOL(models.Model):
    codigoTOL = models.CharField(max_length=10)  # Campo para almacenar un código, con un máximo de 10 caracteres.
    nombre_codigo = models.CharField(max_length=255, null=True, blank=True)  # Nuevo campo agregado que acepta nulos
    activo = models.BooleanField(default=True)  # Soft delete
    
    def __str__(self):
        return f"{self.codigoTOL} - {self.nombre_codigo}"  # Define la representación en cadena del objeto, mostrando el código.
    
    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()

# Clase para manejar códigos secundarios.
class CodigosSecundariosTOL(models.Model):
    codigoTOL = models.CharField(max_length=10)  # Campo para almacenar un código secundario, con un máximo de 10 caracteres.
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