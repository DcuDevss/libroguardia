from pathlib import Path
#from dotenv import load_dotenv
import os

# Carga las variables de entorno desde el archivo .env
#env_path = Path(__file__).resolve().parent.parent / '.env'
#load_dotenv(dotenv_path=env_path)

# Construye rutas dentro del proyecto como BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuraciones rápidas para el desarrollo - no adecuadas para producción//
# Ver https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/


# ADVERTENCIA DE SEGURIDAD: mantén la clave secreta utilizada en producción en secreto.
#SECRET_KEY = os.getenv('SECRET_KEY') nnnn


SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'your-default-secret-key')

# Ruta absoluta a la imagen
#IMAGE_PATH = os.path.join(BASE_DIR, 'comisarias', 'static', 'comisarias', 'images', 'ESCUDO POLICIA.jpeg')//
# ADVERTENCIA DE SEGURIDAD: no ejecutes con debug activado en producción.
DEBUG = True


ALLOWED_HOSTS = []
#el setting esta para desarrollo nuevos cambios
#ALLOWED_HOSTS = ['10.0.200.73', 'localhost', '127.0.0.1']

# Definición de la aplicación

INSTALLED_APPS = [
    'django.contrib.admin',  # Admin de Django
    'django.contrib.auth',  # Sistema de autenticación
    'django.contrib.contenttypes',  # Framework de tipos de contenido
    'django.contrib.sessions',  # Soporte para sesiones
    'django.contrib.messages',  # Framework de mensajes
    'django.contrib.staticfiles',  # Manejo de archivos estáticos
    'compartido',  # Aplicación compartida
    'comisarias',  # Aplicación de comisarías
    'comisariasriogrande',  # Aplicación de comisarías de Rio Grande
    'comisariastolhuin',  # Aplicación de comisarías de Tolhuin
    'divisioncomunicaciones',  # Aplicación de la división de comunicaciones
    'channels',  # Soporte para canales (WebSockets)
    'ckeditor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Middleware de seguridad
    'django.contrib.sessions.middleware.SessionMiddleware',  # Middleware de sesiones
    'django.middleware.locale.LocaleMiddleware',  # Middleware de localización
    'django.middleware.common.CommonMiddleware',  # Middleware común
    'django.middleware.csrf.CsrfViewMiddleware',  # Middleware de CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Middleware de autenticación
    'django.contrib.messages.middleware.MessageMiddleware',  # Middleware de mensajes
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Middleware de protección contra clickjacking
    'compartido.middleware.NoCacheMiddleware',  # Middleware personalizado para no caché
    'compartido.middleware.RedirectAuthenticatedUserMiddleware',  # Middleware personalizado para redirigir usuarios autenticados
    'compartido.middleware.InactivityLogoutMiddleware',  # Middleware personalizado para cerrar sesión por inactividad
    # 'comisarias.middleware.NoCacheMiddleware',  # Añadir este middleware si es necesario
    # 'comisarias.middleware.RedirectAuthenticatedUserMiddleware',  # Añadir este middleware si es necesario
    # 'comisarias.middleware.InactivityLogoutMiddleware',  # Añadir este middleware si es necesario
   
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}


ROOT_URLCONF = 'Libropolicial.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Backend de plantillas de Django
        'DIRS': [BASE_DIR / 'templates'],  # Añadir la ruta de la carpeta de plantillas
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'compartido.context_processors.global_user_permissions',# agreege este nuevo para permisos globales dcu101
            ],
        },
    },
]



#WSGI_APPLICATION = 'Libropolicial.wsgi.application'
#ASGI_APPLICATION = 'Libropolicial.asgi.application'

# Configuración para canales
# settings.py

ASGI_APPLICATION = 'Libropolicial.asgi.application'


# En desarrollo, si no quieres usar Redis todavía
# Puedes usar esto:
# CHANNEL_LAYERS = {
#    'default': {
#        'BACKEND': 'channels.layers.InMemoryChannelLayer',
#    },
# }

# settings.py




# Base de datos
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Utiliza el backend MySQL
        'NAME': 'libro',  # Nombre de la base de datos
        'USER': 'root',  # Usuario de la base de datos vamos
        'PASSWORD': '',  # Contraseña de la base de datos
        'HOST': 'localhost',  # Host de la base de datos
        'PORT': '3306',  # Puerto de la base de datos
    }
}

# Validación de contraseñas
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internacionalización nuevo
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'es-ar'  # Código de idioma para español de Argentina

TIME_ZONE = 'America/Argentina/Buenos_Aires'  # Zona horaria

USE_TZ = False  # Desactiva el uso de la zona horaria UTC
USE_I18N = True  # Habilita la internacionalización
USE_L10N = True  # Habilita la localización

# Archivos estáticos (CSS, JavaScript, Imágenes)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'  # URL para archivos estáticos
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Directorio de archivos estáticos xx
]

# url de firma https://firmar.gob.ar/firmador/#/x
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

import os

# ... otras configuracionesxx

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Tipo de campo de clave primaria predeterminado
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de URL de inicio de sesión
LOGIN_URL = 'login'  # URL de inicio de sesión

# Configuración del motor de sesiones
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# Configuración de canales (WebSockets) 'JustifyRight', 'JustifyBlock',
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', 'SelectAll', 'Scayt']},
            {'name': 'basicstyles', 'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', 'RemoveFormat']},
            {'name': 'paragraph', 'items': ['NumberedList', 'BulletedList', 'Outdent', 'Indent', 'Blockquote', 'CreateDiv', 'JustifyLeft','JustifyCenter',  'BidiLtr', 'BidiRtl', 'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert', 'items': ['Table', 'HorizontalRule', 'SpecialChar']},
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'document', 'items': ['Source']}
        ],
        'height': 250,
        'width': 'auto',
        'font_names': 'Arial/Arial, Helvetica, sans-serif; Times New Roman/Times New Roman, Times, serif; Verdana/Verdana, Geneva, sans-serif; Courier New/Courier New, Courier, monospace',
    },
}
