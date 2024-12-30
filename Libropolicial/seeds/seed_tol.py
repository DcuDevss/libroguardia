import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Libropolicial.settings')

# Initialize Django
django.setup()

# Import the CuartoGuardiaUSH model from compartido
from compartido.models import CodigoPolicialTOL, CodigosSecundariosTOL, CuartoGuardiaTOL

# Seeder function
def run():


    codigos = [
        ('00', 'PERSONA FALLECIDA'),
        ('01', 'HOMICIDIO'),
        ('02', 'SUICIDIO'),
        ('03', 'ROBO'),
        # Agrega más códigos aquí según sea necesario
        ('04', 'ACCIDENTE DE TRANSITO'),
        ('05', 'DAÑOS'),
        ('06', 'CONTRAVENCION'),
        ('07', 'APOYO POLICIAL'),
        ('08', 'VIOLENCIA DE GENERO'),
        ('09', 'VIOLENCIA DE GENERO EN CURSO'),
        ('10', 'VIOLENCIA DE GENERO CON AGRECIONES FISICAS'),
        ('11', 'INCENDIO'),
        ('12', 'PERSONA CON PROHIBICION DE ACERCAMIENTO'),
        ('13', 'PERSONA ARMADA'),
        ('14', 'PERSONA TIRADA EN LA VIA PUBLICA'),
        ('15', 'PERSONA HERIDA'),
        ('16', 'PERSONA CON ABUSO SEXUAL'),
        ('17', 'PERSONA CON INTENTO DE SUICIDIO'),
        ('18', 'PERSONA EXTRAVIADA O PERDIDA'),
        ('19', 'PRESENCIA DE DROGAS'),
        ('20', 'PEDIDO DE AUXILIO'),
        ('21', 'VIOLENCIA FAMILIAR EN CURSO'),
        ('22', 'VIOLENCIA FAMILIAR HISTORICA'),
        ('23', 'AMENAZA DE BOMBA'),
        ('24', 'ARTEFACTO EXPLOSIVO'),
        ('25', 'ANIMALES SUELTOS'),
        ('26', 'CORDON SANITARIO'),
        ('27', 'FUGA DE GAS'),
        ('28', 'USURPACION'),
        ('29', 'PICADAS, EXCESO DE VELOCIDAD/MANIOBRAS PELIGROSAS CON AUTOMOTORES EN VIA PUBLICA'),
        ('30', 'CORTE O DESVIO DE TRANSITO'),
        ('31', 'MANIFESTACION O GRUPOS DE PERSONAS'),
        ('32', 'RUIDOS MOLESTOS'),
        ('33', 'ALARMA'),
        ('34', 'PRESENCIA POLICIAL'),
        ('35', 'FlAGRANCIA')
    ]

    codigos_secundarios = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34','35']
    

    # List of cuartos de guardia to be inserted into the database
    cuartos = ['A', 'B', 'C', 'D']

 # Inserta los códigos para la aplicación USH
    for codigo, nombre in codigos:
        CodigoPolicialTOL.objects.update_or_create(codigoTOL=codigo, defaults={'nombre_codigo': nombre})

    # Inserta los códigos secundarios
    for codigo in codigos_secundarios:
        CodigosSecundariosTOL.objects.get_or_create(codigoTOL=codigo)

    # Inserta cuartos de guardia para la aplicación USH
    for cuarto in cuartos:
        CuartoGuardiaTOL.objects.get_or_create(cuartoTOL=cuarto)

    
    print('Successfully seeded CuartoGuardiaTOL, CodigosSecundariosTOL, CuartoGuardiaTOL  data.')


   
# Execute the function if the script is run directly
if __name__ == '__main__':
    run()
