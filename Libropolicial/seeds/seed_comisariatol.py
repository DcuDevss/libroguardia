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
from comisariastolhuin.models import (
    DependenciasSecundariasTOL, 
    SolicitanteCodigoTOL, ServiciosEmergenciaTOL, InstitucionesHospitalariasTOL, 
    DependenciasMunicipalesTOL, DependenciasProvincialesTOL, InstitucionesFederales
)

#from divisioncomunicaciones.models import CuartoGuardiaTOL

# Función principal para poblar la base de datos
def run():
   
    # Lista de dependencias secundarias
    dependencias_secundariasTOL = ['D.P.C.Th.', 'S.I.C. y N.Th', 'S.B.R.Th.', ]

    # Lista de solicitantes de código
    solicitantes_codigoTOL = ['PARTICULAR', 'COMISARIA', 'OTRO']

    # Lista de servicios de emergencia
    servicios_emergenciaTOL = ['BOMBEROS TOLHUIN']

    # Lista de instituciones hospitalarias
    instituciones_hospitalariasTOL = ['C.M.S. 34']

    # Lista de dependencias municipales
    dependencias_municipalesTOL = ['TRANSITO MUNICIPAL', 'HABILITACIONES COMERCIALES', 'DIRECCION DE TRANSPORTE', 'SEC. DE HABITAT Y ORDENAMIENTO URBANO', 'ZOONOSIS', 'RESGUARDO DE FAUNA', 'AREA DE BROMATOLOGIA', 'SERVICIOS GENERALES', 'SECRETARIA DE EQUINOS', 'JUZGADO ADM. MUNICIPAL DE FALTAS', 'SEC. MEDIO AMBIENTE Y DESARROLLO SUSTENTABLE', 'SECRETARIA DE LA MUJER']

    # Lista de dependencias provinciales
    dependencias_provincialesTOL = ['CAMUZZI TOLHUIN', 'D.P.E', 'TRANSPORTE PROVINCIAL', 'D.P.O.S.S.', 'MANEJO DEL FUEGO', 'RECURSOS NATURALES', 'PROTECCION CIVIL', 'MINISTERIO DE TRABAJO', 'SERVICIOS GENERALES', 'DIR. PROV. DE VIALIDAD', 'I.P.V', 'A.R.E.F', 'O.S.E.F', 'DIV. PROV. PUERTOS' ]

    # Lista de instituciones federales
    instituciones_federales = ['P.S.A', 'G.N.A', 'P.N.A', 'P.F.A', 'A.R.A']



    # Inserta cada dependencia secundaria en la base de datos si no existe
    for dependenciaTOL in dependencias_secundariasTOL:
        DependenciasSecundariasTOL.objects.get_or_create(dependenciaTOL=dependenciaTOL)

    # Inserta cada solicitante de código en la base de datos si no existe
    for solicitanteTOL in solicitantes_codigoTOL:
        SolicitanteCodigoTOL.objects.get_or_create(codigoTOL=solicitanteTOL)

    # Inserta cada servicio de emergencia en la base de datos si no existe
    for servicioTOL in servicios_emergenciaTOL:
        ServiciosEmergenciaTOL.objects.get_or_create(nombre=servicioTOL)

    # Inserta cada institución hospitalaria en la base de datos si no existe
    for institucionTOL in instituciones_hospitalariasTOL:
        InstitucionesHospitalariasTOL.objects.get_or_create(nombre=institucionTOL)

    # Inserta cada dependencia municipal en la base de datos si no existe
    for dependenciaTOL in dependencias_municipalesTOL:
        DependenciasMunicipalesTOL.objects.get_or_create(nombre=dependenciaTOL)

    # Inserta cada dependencia provincial en la base de datos si no existe
    for dependenciaTOL in dependencias_provincialesTOL:
        DependenciasProvincialesTOL.objects.get_or_create(nombre=dependenciaTOL)

    # Inserta cada institución federal en la base de datos si no existe
    for institucionTOL in instituciones_federales:
        InstitucionesFederales.objects.get_or_create(nombre=institucionTOL)

    print('Successfully seeded the database for comisariastolhuin')

# Ejecuta la función principal si el script se está ejecutando directamente
if __name__ == '__main__':
    run()
