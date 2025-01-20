import datetime
from django import template
import re
from django.utils.safestring import mark_safe

# Registra el filtro personalizado para que pueda ser utilizado en las plantillas
register = template.Library()

# Define un filtro de plantilla personalizado llamado 'is_today'
@register.filter
def is_today(value):
    if not value:
        return False
    # Obtiene la fecha y hora actual
    now = datetime.datetime.now()
    # Compara la fecha del valor proporcionado con la fecha actual
    return value.date() == now.date()


# se agrego el resaltado 20/1/25
@register.filter
def highlight(value, query):
    """
    Resalta las palabras que coincidan con la consulta (query) en el texto (value).
    """
    if not query:
        return value  # Devuelve el texto sin cambios si no hay consulta.

    # Asegúrate de que value es una cadena.
    if not isinstance(value, str):
        value = str(value)

    # Escapa caracteres especiales en la consulta.
    escaped_query = re.escape(query)
    
    # Usa re.sub para buscar y reemplazar las coincidencias.
    highlighted = re.sub(
        rf'({escaped_query})',  # Escapa caracteres especiales en la consulta.
        r'<span class="highlight">\1</span>',  # Aplica la clase CSS para resaltar.
        value,
        flags=re.IGNORECASE  # Ignora mayúsculas y minúsculas.
    )
    
    # Marca el resultado como seguro para evitar el escape de HTML.
    return mark_safe(highlighted)
    #fin 20/1/25