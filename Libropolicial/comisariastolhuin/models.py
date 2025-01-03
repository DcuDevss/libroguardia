from django.contrib.auth.models import User  # Importa el modelo User de Django, que representa a los usuarios del sistema.
from django.db import models  # Importa el módulo models de Django, usado para definir modelos de base de datos.
from django.utils import timezone  # Importa la utilidad timezone para manejar fechas y horas según la zona horaria.
#from compartido.models import CuartoGuardiaTOL
from compartido.models import CuartoGuardiaTOL, CodigoPolicialTOL, CodigosSecundariosTOL   # Importa el modelo compartido


# Clase para manejar dependencias secundarias.
class DependenciasSecundariasTOL(models.Model):
    dependenciaTOL = models.CharField(max_length=100)  # Campo para almacenar el nombre de una dependencia secundaria, con un máximo de 100 caracteres.
    activo = models.BooleanField(default=True)  # Soft delete


    def __str__(self):
        return self.dependenciaTOL  # Define la representación en cadena del objeto, mostrando el nombre de la dependencia.
    
    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()


# Clase para manejar solicitantes de códigos.
class SolicitanteCodigoTOL(models.Model):
    codigoTOL = models.CharField(max_length=100)  # Campo para almacenar el nombre o identificador del solicitante de código, con un máximo de 100 caracteres.
    activo = models.BooleanField(default=True)  # Soft delete

    def __str__(self):
        return self.codigoTOL  # Define la representación en cadena del objeto, mostrando el nombre del solicitante.
    
    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()

# Clase para manejar las instituciones hospitalarias.
class InstitucionesHospitalariasTOL(models.Model):
    nombre = models.CharField(max_length=60)  # Campo para almacenar el nombre de una institución hospitalaria, con un máximo de 60 caracteres.
    activo = models.BooleanField(default=True)  # Soft delete
   
    def __str__(self):
        return self.nombre  # Define la representación en cadena del objeto, mostrando el nombre de la institución.
    
    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()

# Clase para manejar dependencias municipales.
class DependenciasMunicipalesTOL(models.Model):
    nombre = models.CharField(max_length=60)  # Campo para almacenar el nombre de una dependencia municipal, con un máximo de 60 caracteres.
    activo = models.BooleanField(default=True)  # Soft delete

    def __str__(self):
        return self.nombre  # Define la representación en cadena del objeto, mostrando el nombre de la dependencia.

    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()

# Clase para manejar dependencias provinciales.
class DependenciasProvincialesTOL(models.Model):
    nombre = models.CharField(max_length=60)  # Campo para almacenar el nombre de una dependencia provincial, con un máximo de 60 caracteres.
    activo = models.BooleanField(default=True)  # Soft delete

    def __str__(self):
        return self.nombre  # Define la representación en cadena del objeto, mostrando el nombre de la dependencia.

    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()

# Clase para manejar los servicios de emergencia.
class ServiciosEmergenciaTOL(models.Model):
    nombre = models.CharField(max_length=60)  # Campo para almacenar el nombre de un servicio de emergencia, con un máximo de 60 caracteres.
    activo = models.BooleanField(default=True)  # Soft delete

    def __str__(self):
        return self.nombre  # Define la representación en cadena del objeto, mostrando el nombre del servicio.
    
    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()


class InstitucionesFederales(models.Model):
    nombre =  models.CharField(max_length=60)
    activo = models.BooleanField(default=True)  # Soft delete
     
    def __str__(self):
        return self.nombre

    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()

class BaseComisariaTOL(models.Model):
    cuartoTOL= models.ForeignKey(CuartoGuardiaTOL, null=True, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(default=timezone.now)  # Almacena la fecha y hora del registro, con la fecha y hora actuales por defecto.
    codigoTOL = models.ForeignKey(CodigoPolicialTOL, null=True, blank=True, on_delete=models.CASCADE)  # Relaciona la comisaría con un código policial; si el código se elimina, se establece a NULL.
    solicitante_codigoTOL = models.ForeignKey(SolicitanteCodigoTOL, null=True, blank=True, on_delete=models.CASCADE)  # Relaciona la comisaría con un solicitante de código; si el solicitante se elimina, se establece a NULL.
    codigos_secundariosTOL= models.ManyToManyField(CodigosSecundariosTOL, blank=True)  # Relaciona la comisaría con múltiples códigos secundarios, permitiendo que el campo quede vacío.
    movil_patrulla = models.CharField(max_length=255, null=True, blank=True)  # Campo para almacenar información sobre el móvil de patrulla, permitiendo que quede vacío.
    a_cargo = models.CharField(max_length=255, null=True, blank=True)  # Campo para almacenar el nombre de la persona a cargo, permitiendo que quede vacío.
    secundante = models.CharField(max_length=255, null=True, blank=True)  # Campo para almacenar el nombre del secundante, permitiendo que quede vacío.
    lugar_codigo = models.CharField(max_length=255, null=True, blank=True)  # Campo para almacenar la ubicación del código, permitiendo que quede vacío.
    descripcion = models.TextField(null=True, blank=True)  # Campo para almacenar una descripción, permitiendo que quede vacío.
    instituciones_intervinientes = models.TextField(null=True, blank=True)  # Campo para almacenar información sobre las instituciones intervinientes, permitiendo que quede vacío.
    tareas_judiciales = models.TextField(null=True, blank=True)  # Campo para almacenar información sobre las tareas judiciales, permitiendo que quede vacío.
    estado = models.BooleanField(default=True)  # Campo booleano que indica si el estado de la comisaría es activo, con un valor por defecto de True.
    firmas = models.TextField(null=True, blank=True)  # Campo para almacenar las firmas, permitiendo que quede vacío.
    latitude = models.FloatField(null=True, blank=True)  # Campo para almacenar la latitud de la comisaría, permitiendo que quede vacío.
    longitude = models.FloatField(null=True, blank=True)  # Campo para almacenar la longitud de la comisaría, permitiendo que quede vacío.
    activo = models.BooleanField(default=True)  # Soft delete para comisarías
    created_at = models.DateTimeField(auto_now_add=True)  # Almacena la fecha y hora en que se creó el registro, asignada automáticamente al crear el objeto.
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='%(class)s_created_records')  # Relaciona la comisaría con el usuario que la creó, permitiendo que quede vacío; si el usuario se elimina, también se elimina la comisaría.
    updated_at = models.DateTimeField(auto_now=True)  # Almacena la fecha y hora en que se actualizó el registro, asignada automáticamente al actualizar el objeto.
    updated_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='%(class)s_updated_records')  # Relaciona la comisaría con el usuario que la actualizó por última vez, permitiendo que quede vacío; si el usuario se elimina, también se elimina la comisaría.

    # Nuevos campos ManyToMany para relacionar la comisaríariogrande con hospitales, dependencias municipales y provinciales, y servicios de emergencia.
    instituciones_hospitalariasTOL = models.ManyToManyField(InstitucionesHospitalariasTOL, blank=True)  # Relaciona la comisaría con múltiples instituciones hospitalarias, permitiendo que el campo quede vacío.
    dependencias_municipalesTOL = models.ManyToManyField(DependenciasMunicipalesTOL, blank=True)  # Relaciona la comisaría con múltiples dependencias municipales, permitiendo que el campo quede vacío.
    dependencias_provincialesTOL = models.ManyToManyField(DependenciasProvincialesTOL, blank=True)  # Relaciona la comisaría con múltiples dependencias provinciales, permitiendo que el campo quede vacío.
    servicios_emergenciaTOL = models.ManyToManyField(ServiciosEmergenciaTOL, blank=True)  # Relaciona la comisaría con múltiples servicios de emergencia, permitiendo que el campo quede vacío.
    instituciones_federales = models.ManyToManyField(InstitucionesFederales, blank=True)  # Relaciona la comisaría con múltiples servicios de insdtituciones federales , permitiendo que el campo quede vacío.
    dependencias_secundariasTOL = models.ManyToManyField(DependenciasSecundariasTOL, blank=True)  # Relaciona la comisaría con múltiples servicios de dependencias secundarias , permitiendo que el campo quede vacío.


    class Meta:
        abstract = True  # Define que esta clase es abstracta, es decir, no se creará una tabla de base de datos para esta clase, sino para sus subclases.


# Subclases concretas de BaseComisaria para cada comisaría. se realizaron cambios
class ComisariaTolhuin(BaseComisariaTOL):
    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()


# Clase para manejar los detalles adicionales de Servicios de Emergencia.
class DetalleServicioEmergenciaTOL(models.Model):
    servicio_emergenciaTOL = models.ForeignKey(ServiciosEmergenciaTOL, on_delete=models.CASCADE)  # Relaciona el detalle con un servicio de emergencia; si el servicio se elimina, también se elimina el detalle.
    comisaria_tolhuin = models.ForeignKey(ComisariaTolhuin, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_servicio_emergenciaTOL')  # Relaciona el detalle con la Comisaría Tolhuin, permitiendo que quede vacío; si la comisaría se elimina, también se elimina el detalle.
    numero_movil_bomberosTOL = models.CharField(max_length=20, null=True, blank=True)  # Campo para almacenar el número de móvil de los bomberos, permitiendo que quede vacío.
    nombre_a_cargo_bomberosTOL = models.CharField(max_length=255, null=True, blank=True)  # Campo para almacenar el nombre de la persona a cargo de los bomberos, permitiendo que quede vacío.

    def __str__(self):
        return f"Servicio de Emergencia TOL: {self.servicio_emergenciaTOL.nombre}"

# Clase para manejar los detalles adicionales de Instituciones Hospitalarias.
class DetalleInstitucionHospitalariaTOL(models.Model):
    institucion_hospitalariaTOL = models.ForeignKey(InstitucionesHospitalariasTOL, on_delete=models.CASCADE)  # Relaciona el detalle con una institución hospitalaria; si la institución se elimina, también se elimina el detalle.
    comisaria_tolhuin = models.ForeignKey(ComisariaTolhuin, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_institucion_hospitalariaTOL')  # Relaciona el detalle con la Comisaría Tolhuin, permitiendo que quede vacío; si la comisaría se elimina, también se elimina el detalle.
    numero_movil_hospitalTOL = models.CharField(max_length=20, null=True, blank=True)  # Campo para almacenar el número de móvil del hospital, permitiendo que quede vacío.
    nombre_a_cargo_hospitalTOL = models.CharField(max_length=255, null=True, blank=True)  # Campo para almacenar el nombre de la persona a cargo del hospital, permitiendo que quede vacío.

    def __str__(self):
        return f"Institución Hospitalaria TOL: {self.institucion_hospitalariaTOL.nombre}"

# Clase para manejar los detalles adicionales de Dependencias Municipales.
class DetalleDependenciaMunicipalTOL(models.Model):
    dependencia_municipalTOL = models.ForeignKey(DependenciasMunicipalesTOL, on_delete=models.CASCADE)  # Relaciona el detalle con una dependencia municipal; si la dependencia se elimina, también se elimina el detalle.
    comisaria_tolhuin = models.ForeignKey(ComisariaTolhuin, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_dependencia_municipalTOL')  # Relaciona el detalle con la Comisaría Tolhuin, permitiendo que quede vacío; si la comisaría se elimina, también se elimina el detalle.
    numero_movil_municipalTOL = models.CharField(max_length=20, null=True, blank=True)  # Campo para almacenar el número de móvil de la dependencia municipal, permitiendo que quede vacío.
    nombre_a_cargo_municipalTOL = models.CharField(max_length=255, null=True, blank=True)  # Campo para almacenar el nombre de la persona a cargo de la dependencia municipal, permitiendo que quede vacío.

    def __str__(self):
        return f"Dependencia Municipal TOL: {self.dependencia_municipalTOL.nombre}"

# Clase para manejar los detalles adicionales de Dependencias Provinciales.
class DetalleDependenciaProvincialTOL(models.Model):
    dependencia_provincialTOL = models.ForeignKey(DependenciasProvincialesTOL, on_delete=models.CASCADE)  # Relaciona el detalle con una dependencia provincial; si la dependencia se elimina, también se elimina el detalle.
    comisaria_tolhuin = models.ForeignKey(ComisariaTolhuin, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_dependencia_provincialTOL')  # Relaciona el detalle con la Comisaría Tolhuin, permitiendo que quede vacío; si la comisaría se elimina, también se elimina el detalle.
    numero_movil_provincialTOL = models.CharField(max_length=20, null=True, blank=True)  # Campo para almacenar el número de móvil de la dependencia provincial, permitiendo que quede vacío.
    nombre_a_cargo_provincialTOL = models.CharField(max_length=255, null=True, blank=True)  # Campo para almacenar el nombre de la persona a cargo de la dependencia provincial, permitiendo que quede vacío.

    def __str__(self):
        return f"Dependencia Provincial TOL: {self.dependencia_provincialTOL.nombre}"

class DetalleInstitucionFederal(models.Model):
    institucion_federal = models.ForeignKey(InstitucionesFederales, on_delete=models.CASCADE)
    comisaria_tolhuin = models.ForeignKey(ComisariaTolhuin, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_institucion_federal')
    numero_movil_federal = models.CharField(max_length=20, null=True, blank=True)
    nombre_a_cargo_federal = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Institución Federal: {self.institucion_federal.nombre}"

class DetalleDependenciaSecundariaTOL(models.Model):
    dependencia_secundariaTOL = models.ForeignKey(DependenciasSecundariasTOL, on_delete=models.CASCADE)
    comisaria_tolhuin = models.ForeignKey(ComisariaTolhuin, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_dependencia_secundariaTOL')
    numero_movil_secundariaTOL = models.CharField(max_length=20, null=True, blank=True)
    nombre_a_cargo_secundariaTOL = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Dependencia Secundaria: {self.dependencia_secundariaTOL.dependenciaTOL}"
