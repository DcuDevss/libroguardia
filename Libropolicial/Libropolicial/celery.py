# libropolicial/celery.py

from __future__ import absolute_import
import os
from celery import Celery

# Establece el archivo de configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Libropolicial.settings')

app = Celery('Libropolicial')

# Lee la configuración de Django para Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubre las tareas dentro de los archivos 'tasks.py' en las apps de Django
app.autodiscover_tasks()
