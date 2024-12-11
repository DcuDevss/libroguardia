import os
import sys
import django

# Agrega el directorio raíz del proyecto al sys.path para que los módulos del proyecto puedan ser importados
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Establece la variable de entorno para las configuraciones de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Libropolicial.settings')

# Inicializa la configuración de Django
django.setup()

# Importa los modelos necesarios
from comisariasriogrande.models import (
    DependenciasSecundariasRG, 
    SolicitanteCodigoRG, ServiciosEmergenciaRG, InstitucionesHospitalariasRG, 
    DependenciasMunicipalesRG, DependenciasProvincialesRG, InstitucionesFederales
)

#from divisioncomunicaciones.models import CuartoGuardiaRG

# Función principal para poblar la base de datos
def run():
   
    # Lista de dependencias secundarias
    dependencias_secundariasRG = ['C.G Y F Nº1 R.G.', 'C.G. y F Nº2 R.G.', 'D.P.C.R.G', 'D.S.E.R.G', 'D.D.C.R.G', 'D.N.D.F.R.G', 'D.B.P.R.G', 'CRIA 1ra R.G', 'CRIA 2da R.G', 'CRIA 3ra R.G', 'CRIA 4ta R.G', 'CRIA 5ta R.G']

    # Lista de solicitantes de código
    solicitantes_codigoRG = ['D.C.R.G', 'PARTICULAR', 'COMISARIA', 'OTRO']

    # Lista de servicios de emergencia
    servicios_emergenciaRG = ['BOMBEROS CMDTE. O.H.ROMERO', 'BOMBEROS 2 DE ABRIL', 'BOMBEROS 12 DE OCTUBRE', 'BOMBEROS 25 DE MAYO', 'BOMBEROS 11 DE ABRIL']

    # Lista de instituciones hospitalarias
    instituciones_hospitalariasRG = ['H.R.R.G', 'CLINICA CEMEP', 'SANATORIO FUEGUINO', 'LOS ALAMOS']

    # Lista de dependencias municipales
    dependencias_municipalesRG = ['TRANSITO MUNICIPAL', 'HABILITACIONES COMERCIALES', 'DIRECCION DE TRANSPORTE', 'SEC. DE HABITAT Y ORDENAMIENTO URBANO', 'ZOONOSIS', 'RESGUARDO DE FAUNA', 'AREA DE BROMATOLOGIA', 'SERVICIOS GENERALES', 'SECRETARIA DE EQUINOS', 'JUZGADO ADM. MUNICIPAL DE FALTAS', 'SEC. MEDIO AMBIENTE Y DESARROLLO SUSTENTABLE', 'SECRETARIA DE LA MUJER']

    # Lista de dependencias provinciales
    dependencias_provincialesRG = ['CAMUZZI R.G', 'D.P.E.R.G', 'TRANSPORTE PROVINCIAL', 'D.P.O.S.S.R.G', 'MANEJO DEL FUEGO', 'RECURSOS NATURALES', 'PROTECCION CIVIL', 'MINISTERIO DE TRABAJO', 'SERVICIOS GENERALES', 'DIR. PROV. DE VIALIDAD', 'I.P.V', 'A.R.E.F', 'O.S.E.F', 'DIV. PROV. PUERTOS' ]

    # Lista de instituciones federales
    instituciones_federales = ['P.S.A', 'G.N.A', 'P.N.A', 'P.F.A', 'A.R.A']



    # Inserta cada dependencia secundaria en la base de datos si no existe
    for dependenciaRG in dependencias_secundariasRG:
        DependenciasSecundariasRG.objects.get_or_create(dependenciaRG=dependenciaRG)

    # Inserta cada solicitante de código en la base de datos si no existe
    for solicitanteRG in solicitantes_codigoRG:
        SolicitanteCodigoRG.objects.get_or_create(codigoRG=solicitanteRG)

    # Inserta cada servicio de emergencia en la base de datos si no existe
    for servicioRG in servicios_emergenciaRG:
        ServiciosEmergenciaRG.objects.get_or_create(nombre=servicioRG)

    # Inserta cada institución hospitalaria en la base de datos si no existe
    for institucionRG in instituciones_hospitalariasRG:
        InstitucionesHospitalariasRG.objects.get_or_create(nombre=institucionRG)

    # Inserta cada dependencia municipal en la base de datos si no existe
    for dependenciaRG in dependencias_municipalesRG:
        DependenciasMunicipalesRG.objects.get_or_create(nombre=dependenciaRG)

    # Inserta cada dependencia provincial en la base de datos si no existe
    for dependenciaRG in dependencias_provincialesRG:
        DependenciasProvincialesRG.objects.get_or_create(nombre=dependenciaRG)

    # Inserta cada institución federal en la base de datos si no existe
    for institucionRG in instituciones_federales:
        InstitucionesFederales.objects.get_or_create(nombre=institucionRG)

    print('Successfully seeded the database for comisariasriogrande')

# Ejecuta la función principal si el script se está ejecutando directamente
if __name__ == '__main__':
    run()
