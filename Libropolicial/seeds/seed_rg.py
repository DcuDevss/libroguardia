import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Libropolicial.settings')

# Initialize Django
django.setup()

# Import models for RG
from compartido.models import CodigoPolicialRG, CodigosSecundariosRG, CuartoGuardiaRG

# Seeder function for RG data
def run():
    # Data for RG
    codigos = [
        ('00', 'PERSONA FALLECIDA'),
        ('01', 'HOMICIDIO'),
        ('02', 'SUICIDIO'),
        ('03', 'ROBO'),
        # Agrega más códigos según sea necesario
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
        ('35', 'FLAGRANCIA')
    ]

    codigos_secundarios = [
        '00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', 
        '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', 
        '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', 
        '33', '34', '35'
    ]

    cuartos = ['A', 'B', 'C', 'D']

    # Inserta cada código en la base de datos si no existe
    for codigo, nombre in codigos:
        CodigoPolicialRG.objects.update_or_create(codigoRG=codigo, defaults={'nombre_codigo': nombre})

    # Inserta cada código secundario en la base de datos si no existe
    for codigo in codigos_secundarios:
        CodigosSecundariosRG.objects.get_or_create(codigoRG=codigo)

    # Insert each cuarto into the database if it does not exist
    for cuarto in cuartos:
        CuartoGuardiaRG.objects.get_or_create(cuartoRG=cuarto)

    print('Successfully seeded CuartoGuardiaRG, CodigosSecundariosRG, CuartoGuardiaRG  data.')

# Execute the function if the script is run directly
if __name__ == '__main__':
    run()
