# comisarias/tasks.py

from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.utils import timezone
from .views import generate_comisaria_primera_pdf_download
from django.core.files.storage import default_storage

@shared_task
def generate_daily_comisaria_tolhuin_pdf():
    today = timezone.now()
    filename = f"parte-diario-{today.strftime('%d-%m-%Y')}.pdf"
    pdf_content = generate_comisaria_tolhuin_pdf_download()  # Ajusta esta línea según sea necesario
    with default_storage.open(f'reports/{filename}', 'wb') as f:
        f.write(pdf_content.getvalue())
