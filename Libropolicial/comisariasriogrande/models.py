from django.contrib.auth.models import User  # Importa el modelo User de Django, que representa a los usuarios del sistema.
from django.db import models  # Importa el módulo models de Django, usado para definir modelos de base de datos.
from django.utils import timezone  # Importa la utilidad timezone para manejar fechas y horas según la zona horaria.
#from compartido.models import CuartoGuardiaRG
from compartido.models import CuartoGuardiaRG, CodigoPolicialRG, CodigosSecundariosRG   # Importa el modelo compartido


# Clase para manejar dependencias secundarias.
class DependenciasSecundariasRG(models.Model):
    dependenciaRG = models.CharField(max_length=100)  # Campo para almacenar el nombre de una dependencia secundaria, con un máximo de 100 caracteres.
    activo = models.BooleanField(default=True)  # Soft delete


    def __str__(self):
        return self.dependenciaRG  # Define la representación en cadena del objeto, mostrando el nombre de la dependencia.
    
    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()


# Clase para manejar solicitantes de códigos.
class SolicitanteCodigoRG(models.Model):
    codigoRG = models.CharField(max_length=100)  # Campo para almacenar el nombre o identificador del solicitante de código, con un máximo de 100 caracteres.
    activo = models.BooleanField(default=True)  # Soft delete

    def __str__(self):
        return self.codigoRG  # Define la representación en cadena del objeto, mostrando el nombre del solicitante.
    
    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()

# Clase para manejar las instituciones hospitalarias.
class InstitucionesHospitalariasRG(models.Model):
    nombre = models.CharField(max_length=60)  # Campo para almacenar el nombre de una institución hospitalaria, con un máximo de 60 caracteres.
    activo = models.BooleanField(default=True)  # Soft delete
   
    def __str__(self):
        return self.nombre  # Define la representación en cadena del objeto, mostrando el nombre de la institución.
    
    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()

# Clase para manejar dependencias municipales.
class DependenciasMunicipalesRG(models.Model):
    nombre = models.CharField(max_length=60)  # Campo para almacenar el nombre de una dependencia municipal, con un máximo de 60 caracteres.
    activo = models.BooleanField(default=True)  # Soft delete

    def __str__(self):
        return self.nombre  # Define la representación en cadena del objeto, mostrando el nombre de la dependencia.

    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()

# Clase para manejar dependencias provinciales.
class DependenciasProvincialesRG(models.Model):
    nombre = models.CharField(max_length=60)  # Campo para almacenar el nombre de una dependencia provincial, con un máximo de 60 caracteres.
    activo = models.BooleanField(default=True)  # Soft delete

    def __str__(self):
        return self.nombre  # Define la representación en cadena del objeto, mostrando el nombre de la dependencia.

    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()

# Clase para manejar los servicios de emergencia.
class ServiciosEmergenciaRG(models.Model):
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

class BaseComisariaRG(models.Model):
    cuartoRG= models.ForeignKey(CuartoGuardiaRG, null=True, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(default=timezone.now)  # Almacena la fecha y hora del registro, con la fecha y hora actuales por defecto.
    codigoRG = models.ForeignKey(CodigoPolicialRG, null=True, blank=True, on_delete=models.CASCADE)  # Relaciona la comisaría con un código policial; si el código se elimina, se establece a NULL.
    solicitante_codigoRG = models.ForeignKey(SolicitanteCodigoRG, null=True, blank=True, on_delete=models.CASCADE)  # Relaciona la comisaría con un solicitante de código; si el solicitante se elimina, se establece a NULL.
    codigos_secundariosRG= models.ManyToManyField(CodigosSecundariosRG, blank=True)  # Relaciona la comisaría con múltiples códigos secundarios, permitiendo que el campo quede vacío.
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
    instituciones_hospitalariasRG = models.ManyToManyField(InstitucionesHospitalariasRG, blank=True)  # Relaciona la comisaría con múltiples instituciones hospitalarias, permitiendo que el campo quede vacío.
    dependencias_municipalesRG = models.ManyToManyField(DependenciasMunicipalesRG, blank=True)  # Relaciona la comisaría con múltiples dependencias municipales, permitiendo que el campo quede vacío.
    dependencias_provincialesRG = models.ManyToManyField(DependenciasProvincialesRG, blank=True)  # Relaciona la comisaría con múltiples dependencias provinciales, permitiendo que el campo quede vacío.
    servicios_emergenciaRG = models.ManyToManyField(ServiciosEmergenciaRG, blank=True)  # Relaciona la comisaría con múltiples servicios de emergencia, permitiendo que el campo quede vacío.
    instituciones_federales = models.ManyToManyField(InstitucionesFederales, blank=True)  # Relaciona la comisaría con múltiples servicios de insdtituciones federales , permitiendo que el campo quede vacío.
    dependencias_secundariasRG = models.ManyToManyField(DependenciasSecundariasRG, blank=True)  # Relaciona la comisaría con múltiples servicios de dependencias secundarias , permitiendo que el campo quede vacío.


    class Meta:
        abstract = True  # Define que esta clase es abstracta, es decir, no se creará una tabla de base de datos para esta clase, sino para sus subclases.


# Subclases concretas de BaseComisaria para cada comisaría. se realizaron cambios
class ComisariaPrimeraRG(BaseComisariaRG):
    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()

class ComisariaSegundaRG(BaseComisariaRG):
    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()

class ComisariaTerceraRG(BaseComisariaRG):
    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()

class ComisariaCuartaRG(BaseComisariaRG):
    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()

class ComisariaQuintaRG(BaseComisariaRG):
    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()

# Clase para manejar los detalles adicionales de Servicios de Emergencia.
class DetalleServicioEmergenciaRG(models.Model):
    servicio_emergenciaRG = models.ForeignKey(ServiciosEmergenciaRG, on_delete=models.CASCADE)  # Relaciona el detalle con un servicio de emergencia; si el servicio se elimina, también se elimina el detalle.
    comisaria_primeraRG = models.ForeignKey(ComisariaPrimeraRG, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_servicio_emergenciaRG')  # Relaciona el detalle con la Comisaría Primera, permitiendo que quede vacío; si la comisaría se elimina, también se elimina el detalle.
    comisaria_segundaRG = models.ForeignKey(ComisariaSegundaRG, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_servicio_emergenciaRG')  # Relaciona el detalle con la Comisaría Segunda, permitiendo que quede vacío; si la comisaría se elimina, también se elimina el detalle.
    comisaria_terceraRG = models.ForeignKey(ComisariaTerceraRG, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_servicio_emergenciaRG')  # Relaciona el detalle con la Comisaría Tercera, permitiendo que quede vacío; si la comisaría se elimina, también se elimina el detalle.
    comisaria_cuartaRG = models.ForeignKey(ComisariaCuartaRG, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_servicio_emergenciaRG')  # Relaciona el detalle con la Comisaría Cuarta, permitiendo que quede vacío; si la comisaría se elimina, también se elimina el detalle.
    comisaria_quintaRG = models.ForeignKey(ComisariaQuintaRG, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_servicio_emergenciaRG')  # Relaciona el detalle con la Comisaría Quinta, permitiendo que quede vacío; si la comisaría se elimina, también se elimina el detalle.
    numero_movil_bomberosRG = models.CharField(max_length=20, null=True, blank=True)  # Campo para almacenar el número de móvil de los bomberos, permitiendo que quede vacío.
    nombre_a_cargo_bomberosRG = models.CharField(max_length=255, null=True, blank=True)  # Campo para almacenar el nombre de la persona a cargo de los bomberos, permitiendo que quede vacío.

    def __str__(self):
        return f"Servicio de Emergencia RG: {self.servicio_emergenciaRG.nombre}"

# Clase para manejar los detalles adicionales de Instituciones Hospitalarias.
class DetalleInstitucionHospitalariaRG(models.Model):
    institucion_hospitalariaRG = models.ForeignKey(InstitucionesHospitalariasRG, on_delete=models.CASCADE)  # Relaciona el detalle con una institución hospitalaria; si la institución se elimina, también se elimina el detalle.
    comisaria_primeraRG = models.ForeignKey(ComisariaPrimeraRG, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_institucion_hospitalariaRG')  # Relaciona el detalle con la Comisaría Primera, permitiendo que quede vacío; si la comisaría se elimina, también se elimina el detalle.
    comisaria_segundaRG = models.ForeignKey(ComisariaSegundaRG, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_institucion_hospitalariaRG')  # Relaciona el detalle con la Comisaría Segunda, permitiendo que quede vacío; si la comisaría se elimina, también se elimina el detalle.
    comisaria_terceraRG = models.ForeignKey(ComisariaTerceraRG, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_institucion_hospitalariaRG')  # Relaciona el detalle con la Comisaría Tercera, permitiendo que quede vacío; si la comisaría se elimina, también se elimina el detalle.
    comisaria_cuartaRG = models.ForeignKey(ComisariaCuartaRG, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_institucion_hospitalariaRG')  # Relaciona el detalle con la Comisaría Cuarta, permitiendo que quede vacío; si la comisaría se elimina, también se elimina el detalle.
    comisaria_quintaRG = models.ForeignKey(ComisariaQuintaRG, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_institucion_hospitalariaRG')  # Relaciona el detalle con la Comisaría Quinta, permitiendo que quede vacío; si la comisaría se elimina, también se elimina el detalle.
    numero_movil_hospitalRG = models.CharField(max_length=20, null=True, blank=True)  # Campo para almacenar el número de móvil del hospital, permitiendo que quede vacío.
    nombre_a_cargo_hospitalRG = models.CharField(max_length=255, null=True, blank=True)  # Campo para almacenar el nombre de la persona a cargo del hospital, permitiendo que quede vacío.

    def __str__(self):
        return f"Institución Hospitalaria RG: {self.institucion_hospitalariaRG.nombre}"

# Clase para manejar los detalles adicionales de Dependencias Municipales.
class DetalleDependenciaMunicipalRG(models.Model):
    dependencia_municipalRG = models.ForeignKey(DependenciasMunicipalesRG, on_delete=models.CASCADE)  # Relaciona el detalle con una dependencia municipal; si la dependencia se elimina, también se elimina el detalle.
    comisaria_primeraRG = models.ForeignKey(ComisariaPrimeraRG, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_dependencia_municipalRG')  # Relaciona el detalle con la Comisaría Primera, permitiendo que quede vacío; si la comisaría se elimina, también se elimina el detalle.
    comisaria_segundaRG = models.ForeignKey(ComisariaSegundaRG, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_dependencia_municipalRG')  # Relaciona el detalle con la Comisaría Segunda, permitiendo que quede vacío; si la comisaría se elimina, también se elimina el detalle.
    comisaria_terceraRG = models.ForeignKey(ComisariaTerceraRG, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_dependencia_municipalRG')  # Relaciona el detalle con la Comisaría Tercera, permitiendo que quede vacío; si la comisaría se elimina, también se elimina el detalle.
    comisaria_cuartaRG = models.ForeignKey(ComisariaCuartaRG, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_dependencia_municipalRG')  # Relaciona el detalle con la Comisaría Cuarta, permitiendo que quede vacío; si la comisaría se elimina, también se elimina el detalle.
    comisaria_quintaRG = models.ForeignKey(ComisariaQuintaRG, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_dependencia_municipalRG')  # Relaciona el detalle con la Comisaría Quinta, permitiendo que quede vacío; si la comisaría se elimina, también se elimina el detalle.
    numero_movil_municipalRG = models.CharField(max_length=20, null=True, blank=True)  # Campo para almacenar el número de móvil de la dependencia municipal, permitiendo que quede vacío.
    nombre_a_cargo_municipalRG = models.CharField(max_length=255, null=True, blank=True)  # Campo para almacenar el nombre de la persona a cargo de la dependencia municipal, permitiendo que quede vacío.

    def __str__(self):
        return f"Dependencia Municipal RG: {self.dependencia_municipalRG.nombre}"

# Clase para manejar los detalles adicionales de Dependencias Provinciales.
class DetalleDependenciaProvincialRG(models.Model):
    dependencia_provincialRG = models.ForeignKey(DependenciasProvincialesRG, on_delete=models.CASCADE)  # Relaciona el detalle con una dependencia provincial; si la dependencia se elimina, también se elimina el detalle.
    comisaria_primeraRG = models.ForeignKey(ComisariaPrimeraRG, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_dependencia_provincialRG')  # Relaciona el detalle con la Comisaría Primera, permitiendo que quede vacío; si la comisaría se elimina, también se elimina el detalle.
    comisaria_segundaRG = models.ForeignKey(ComisariaSegundaRG, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_dependencia_provincialRG')  # Relaciona el detalle con la Comisaría Segunda, permitiendo que quede vacío; si la comisaría se elimina, también se elimina el detalle.
    comisaria_terceraRG = models.ForeignKey(ComisariaTerceraRG, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_dependencia_provincialRG')  # Relaciona el detalle con la Comisaría Tercera, permitiendo que quede vacío; si la comisaría se elimina, también se elimina el detalle.
    comisaria_cuartaRG = models.ForeignKey(ComisariaCuartaRG, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_dependencia_provincialRG')  # Relaciona el detalle con la Comisaría Cuarta, permitiendo que quede vacío; si la comisaría se elimina, también se elimina el detalle.
    comisaria_quintaRG = models.ForeignKey(ComisariaQuintaRG, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_dependencia_provincialRG')  # Relaciona el detalle con la Comisaría Quinta, permitiendo que quede vacío; si la comisaría se elimina, también se elimina el detalle.
    numero_movil_provincialRG = models.CharField(max_length=20, null=True, blank=True)  # Campo para almacenar el número de móvil de la dependencia provincial, permitiendo que quede vacío.
    nombre_a_cargo_provincialRG = models.CharField(max_length=255, null=True, blank=True)  # Campo para almacenar el nombre de la persona a cargo de la dependencia provincial, permitiendo que quede vacío.

    def __str__(self):
        return f"Dependencia Provincial RG: {self.dependencia_provincialRG.nombre}"

class DetalleInstitucionFederal(models.Model):
    institucion_federal = models.ForeignKey(InstitucionesFederales, on_delete=models.CASCADE)
    comisaria_primeraRG = models.ForeignKey(ComisariaPrimeraRG, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_institucion_federal')
    comisaria_segundaRG = models.ForeignKey(ComisariaSegundaRG, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_institucion_federal')
    comisaria_terceraRG = models.ForeignKey(ComisariaTerceraRG, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_institucion_federal')
    comisaria_cuartaRG = models.ForeignKey(ComisariaCuartaRG, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_institucion_federal')
    comisaria_quintaRG = models.ForeignKey(ComisariaQuintaRG, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_institucion_federal')   
    numero_movil_federal = models.CharField(max_length=20, null=True, blank=True)
    nombre_a_cargo_federal = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Institución Federal: {self.institucion_federal.nombre}"

class DetalleDependenciaSecundariaRG(models.Model):
    dependencia_secundariaRG = models.ForeignKey(DependenciasSecundariasRG, on_delete=models.CASCADE)
    comisaria_primeraRG = models.ForeignKey(ComisariaPrimeraRG, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_dependencia_secundariaRG')
    comisaria_segundaRG = models.ForeignKey(ComisariaSegundaRG, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_dependencia_secundariaRG')
    comisaria_terceraRG = models.ForeignKey(ComisariaTerceraRG, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_dependencia_secundariaRG')
    comisaria_cuartaRG = models.ForeignKey(ComisariaCuartaRG, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_dependencia_secundariaRG')
    comisaria_quintaRG = models.ForeignKey(ComisariaQuintaRG, null=True, blank=True, on_delete=models.CASCADE, related_name='detalles_dependencia_secundariaRG')    
    numero_movil_secundariaRG = models.CharField(max_length=20, null=True, blank=True)
    nombre_a_cargo_secundariaRG = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Dependencia Secundaria: {self.dependencia_secundariaRG.dependenciaRG}"
