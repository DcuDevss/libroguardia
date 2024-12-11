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
from comisarias.models import (
    DependenciasSecundarias, 
    SolicitanteCodigo, ServiciosEmergencia, InstitucionesHospitalarias, 
    DependenciasMunicipales, DependenciasProvinciales, InstitucionesFederales
)

#from divisioncomunicaciones.models import CuartoGuardiaUSH

# Función principal para poblar la base de datos
def run():
   
    # Lista de dependencias secundarias
    dependencias_secundarias = ['C.G. y F.Nº1U.', 'C.G. y F.Nº2U.', 'D.P.C.U', 'D.S.E.U', 'D.D.C.U', 'D.N.D.F.U', 'CRIA 1ra', 'CRIA 2da', 'CRIA 3ra', 'CRIA 4ta', 'CRIA 5ta']

    # Lista de solicitantes de código
    solicitantes_codigo = ['D.C.U', 'PARTICULAR', 'COMISARIA', 'OTRO']

    # Lista de servicios de emergencia
    servicios_emergencia = ['BOMBEROS 2 DE ABRIL', 'BOMBEROS ZONA NORTE', 'BOMBEROS ZONA CENTRO', 'DTO. KUANIP']

    # Lista de instituciones hospitalarias
    instituciones_hospitalarias = ['H.R.U', 'CLINICA SAN JORGE', 'BAHIA SALUD', 'FUEGUINA SALUD', 'SANOS']

    # Lista de dependencias municipales
    dependencias_municipales = ['TRANSITO MUNICIPAL', 'HABILITACIONES COMERCIALES', 'DIRECCION DE TRANSPORTE', 'SEC. DE HABITAT Y ORDENAMIENTO URBANO', 'ZOONOSIS', 'RESGUARDO DE FAUNA', 'AREA DE BROMATOLOGIA', 'SERVICIOS GENERALES', 'SECRETARIA DE EQUINOS', 'JUZGADO ADM. MUNICIPAL DE FALTAS', 'SEC. MEDIO AMBIENTE Y DESARROLLO SUSTENTABLE', 'SECRETARIA DE LA MUJER']

    # Lista de dependencias provinciales
    dependencias_provinciales = ['CAMUZZI USHUAIA', 'D.P.E', 'TRANSPORTE PROVINCIAL', 'D.P.O.S.S.', 'MANEJO DEL FUEGO', 'RECURSOS NATURALES', 'PROTECCION CIVIL', 'MINISTERIO DE TRABAJO', 'SERVICIOS GENERALES', 'DIR. PROV. DE VIALIDAD', 'I.P.V', 'A.R.E.F', 'O.S.E.F', 'DIV. PROV. PUERTOS' ]

    # Lista de instituciones federales
    instituciones_federales = ['P.S.A', 'G.N.A', 'P.N.A', 'P.F.A', 'A.R.A']



    # Inserta cada dependencia secundaria en la base de datos si no existe
    for dependencia in dependencias_secundarias:
        DependenciasSecundarias.objects.get_or_create(dependencia=dependencia)

    # Inserta cada solicitante de código en la base de datos si no existe
    for solicitante in solicitantes_codigo:
        SolicitanteCodigo.objects.get_or_create(codigo=solicitante)

    # Inserta cada servicio de emergencia en la base de datos si no existe
    for servicio in servicios_emergencia:
        ServiciosEmergencia.objects.get_or_create(nombre=servicio)

    # Inserta cada institución hospitalaria en la base de datos si no existe
    for institucion in instituciones_hospitalarias:
        InstitucionesHospitalarias.objects.get_or_create(nombre=institucion)

    # Inserta cada dependencia municipal en la base de datos si no existe
    for dependencia in dependencias_municipales:
        DependenciasMunicipales.objects.get_or_create(nombre=dependencia)

    # Inserta cada dependencia provincial en la base de datos si no existe
    for dependencia in dependencias_provinciales:
        DependenciasProvinciales.objects.get_or_create(nombre=dependencia)

    # Inserta cada institución federal en la base de datos si no existe
    for institucion in instituciones_federales:
        InstitucionesFederales.objects.get_or_create(nombre=institucion)

    print('Successfully seeded the database for comisarias')

# Ejecuta la función principal si el script se está ejecutando directamente
if __name__ == '__main__':
    run()
