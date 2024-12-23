# Libropolicial/comisariasriogrande/urls.py
from django.urls import path
from . import views
from .views import (
    # Funciones para generar PDFs y firmas
    generate_comisaria_primeraRG_pdf_view, generate_comisaria_primeraRG_pdf_download,
    generate_comisaria_segundaRG_pdf_view, generate_comisaria_segundaRG_pdf_download,
    generate_comisaria_terceraRG_pdf_view, generate_comisaria_terceraRG_pdf_download,
    generate_comisaria_cuartaRG_pdf_view, generate_comisaria_cuartaRG_pdf_download,
    generate_comisaria_quintaRG_pdf_view, generate_comisaria_quintaRG_pdf_download,
    generate_comisaria_primeraRG_pdf_download_previous_day, generate_comisaria_segundaRG_pdf_download_previous_day,
    generate_comisaria_terceraRG_pdf_download_previous_day, generate_comisaria_cuartaRG_pdf_download_previous_day,
    generate_comisaria_quintaRG_pdf_download_previous_day,
    sign_comisaria_primeraRG, sign_comisaria_segundaRG, sign_comisaria_terceraRG, sign_comisaria_cuartaRG, sign_comisaria_quintaRG,
    
    # Otras funciones y vistas
    subir_pdfRG, ver_pdfsRG, mostrar_pdfRG,
    
    # Vistas de listas y CRUD de comisarías
    ComisariaPrimeraRGListView, ComisariaSegundaRGListView, ComisariaTerceraRGListView,
    ComisariaCuartaRGListView, ComisariaQuintaRGListView, ComisariasCompletaRGListView,
    
    # Vistas de creación
    ComisariaPrimeraRGCreateView, ComisariaSegundaRGCreateView, ComisariaTerceraRGCreateView,
    ComisariaCuartaRGCreateView, ComisariaQuintaRGCreateView,
    
    # Vistas de actualización
    ComisariaPrimeraRGUpdateView, ComisariaSegundaRGUpdateView, ComisariaTerceraRGUpdateView,
    ComisariaCuartaRGUpdateView, ComisariaQuintaRGUpdateView,
    
    # Vistas de detalle
    ComisariaPrimeraRGDetailView, ComisariaSegundaRGDetailView, ComisariaTerceraRGDetailView,
    ComisariaCuartaRGDetailView, ComisariaQuintaRGDetailView,

     #softdelete
    eliminar_comisaria_primeraRG, eliminar_comisaria_segundaRG, eliminar_comisaria_terceraRG, eliminar_comisaria_cuartaRG,
    eliminar_comisaria_quintaRG
)

urlpatterns = [
    # Comisaría Primera
    path('primeraRG/', ComisariaPrimeraRGListView.as_view(), name='comisaria_primeraRG_list'),
    path('primeraRG/create/', ComisariaPrimeraRGCreateView.as_view(), name='comisaria_primeraRG_create'),
    path('primeraRG/edit/<int:pk>/', ComisariaPrimeraRGUpdateView.as_view(), name='comisaria_primeraRG_edit'),
    path('comisariasriogrande/primeraRG/detalle/<int:pk>/', ComisariaPrimeraRGDetailView.as_view(), name='comisaria_primeraRG_detail'),
    path('primeraRG/reporte/view/', generate_comisaria_primeraRG_pdf_view, name='generate_comisaria_primeraRG_pdf_view'),
    path('primeraRG/reporte/download/', generate_comisaria_primeraRG_pdf_download, name='generate_comisaria_primeraRG_pdf_download'),
    path('comisariasriogrande/primeraRG/descargar-dia-anterior/', generate_comisaria_primeraRG_pdf_download_previous_day, name='generate_comisaria_primeraRG_pdf_download_previous_day'),
    path('primeraRG/firmar/<int:pk>/', sign_comisaria_primeraRG, name='comisaria_primeraRG_sign'),
    path('primeraRG/eliminar/<int:pk>/', eliminar_comisaria_primeraRG, name='comisaria_primeraRG_eliminar'),


    # Comisaría Segunda
    path('segundaRG/', ComisariaSegundaRGListView.as_view(), name='comisaria_segundaRG_list'),
    path('segundaRG/nuevo/', ComisariaSegundaRGCreateView.as_view(), name='comisaria_segundaRG_create'),
    path('segundaRG/editar/<int:pk>/', ComisariaSegundaRGUpdateView.as_view(), name='comisaria_segundaRG_edit'),
    path('comisariasriogrande/segundaRG/detalle/<int:pk>/', ComisariaSegundaRGDetailView.as_view(), name='comisaria_segundaRG_detail'),
    path('segundaRG/reporte/', generate_comisaria_segundaRG_pdf_view, name='generate_comisaria_segundaRG_pdf_view'),
    path('segundaRG/reporte/download/', generate_comisaria_segundaRG_pdf_download, name='generate_comisaria_segundaRG_pdf_download'),
    path('comisariasriogrande/segundaRG/descargar-dia-anterior/', generate_comisaria_segundaRG_pdf_download_previous_day, name='generate_comisaria_segundaRG_pdf_download_previous_day'),
    path('segundaRG/firmar/<int:pk>/', sign_comisaria_segundaRG, name='comisaria_segundaRG_sign'),
    path('segundaRG/eliminar/<int:pk>/', eliminar_comisaria_segundaRG, name='comisaria_segundaRG_eliminar'),

    # Comisaría Tercera
    path('terceraRG/', ComisariaTerceraRGListView.as_view(), name='comisaria_terceraRG_list'),
    path('terceraRG/nuevo/', ComisariaTerceraRGCreateView.as_view(), name='comisaria_terceraRG_create'),
    path('terceraRG/editar/<int:pk>/', ComisariaTerceraRGUpdateView.as_view(), name='comisaria_terceraRG_edit'),
    path('comisariasriogrande/terceraRG/detalle/<int:pk>/', ComisariaTerceraRGDetailView.as_view(), name='comisaria_terceraRG_detail'),
    path('terceraRG/reporte/', generate_comisaria_terceraRG_pdf_view, name='generate_comisaria_terceraRG_pdf_view'),
    path('terceraRG/reporte/download/', generate_comisaria_terceraRG_pdf_download, name='generate_comisaria_terceraRG_pdf_download'),
    path('comisariasriogrande/terceraRG/descargar-dia-anterior/', generate_comisaria_terceraRG_pdf_download_previous_day, name='generate_comisaria_terceraRG_pdf_download_previous_day'),
    path('terceraRG/firmar/<int:pk>/', sign_comisaria_terceraRG, name='comisaria_terceraRG_sign'),
    path('terceraRG/eliminar/<int:pk>/', eliminar_comisaria_terceraRG, name='comisaria_terceraRG_eliminar'),

    # Comisaría Cuarta
    path('cuartaRG/', ComisariaCuartaRGListView.as_view(), name='comisaria_cuartaRG_list'),
    path('cuartaRG/nuevo/', ComisariaCuartaRGCreateView.as_view(), name='comisaria_cuartaRG_create'),
    path('cuartaRG/editar/<int:pk>/', ComisariaCuartaRGUpdateView.as_view(), name='comisaria_cuartaRG_edit'),
    path('comisariasriogrande/cuartaRG/detalle/<int:pk>/', ComisariaCuartaRGDetailView.as_view(), name='comisaria_cuartaRG_detail'),
    path('cuartaRG/reporte/', generate_comisaria_cuartaRG_pdf_view, name='generate_comisaria_cuartaRG_pdf_view'),
    path('cuartaRG/reporte/download/', generate_comisaria_cuartaRG_pdf_download, name='generate_comisaria_cuartaRG_pdf_download'),
    path('comisariasriogrande/cuartaRG/descargar-dia-anterior/', generate_comisaria_cuartaRG_pdf_download_previous_day, name='generate_comisaria_cuartaRG_pdf_download_previous_day'),
    path('cuartaRG/firmar/<int:pk>/', sign_comisaria_cuartaRG, name='comisaria_cuartaRG_sign'),
    path('cuartaRG/eliminar/<int:pk>/', eliminar_comisaria_cuartaRG, name='comisaria_cuartaRG_eliminar'),


    # Comisaría Quinta
    path('quintaRG/', ComisariaQuintaRGListView.as_view(), name='comisaria_quintaRG_list'),
    path('quintaRG/nuevo/', ComisariaQuintaRGCreateView.as_view(), name='comisaria_quintaRG_create'),
    path('quintaRG/editar/<int:pk>/', ComisariaQuintaRGUpdateView.as_view(), name='comisaria_quintaRG_edit'),
    path('comisariasriogrande/quintaRG/detalle/<int:pk>/', ComisariaQuintaRGDetailView.as_view(), name='comisaria_quintaRG_detail'),
    path('quintaRG/reporte/', generate_comisaria_quintaRG_pdf_view, name='generate_comisaria_quintaRG_pdf_view'),
    path('quintaRG/reporte/download/', generate_comisaria_quintaRG_pdf_download, name='generate_comisaria_quintaRG_pdf_download'),
    path('comisariasriogrande/quintaRG/descargar-dia-anterior/', generate_comisaria_quintaRG_pdf_download_previous_day, name='generate_comisaria_quintaRG_pdf_download_previous_day'),
    path('quintaRG/firmar/<int:pk>/', sign_comisaria_quintaRG, name='comisaria_quintaRG_sign'),
    path('quintaRG/eliminar/<int:pk>/', eliminar_comisaria_quintaRG, name='comisaria_quintaRG_eliminar'),


    # Otras rutas
    path('subir-pdfRG/', subir_pdfRG, name='subir_pdfRG'),
    path('ver-pdfsRG/', ver_pdfsRG, name='ver_pdfsRG'),  # Nueva URL para ver los PDFs
    path('mostrar-pdfRG/<int:pdf_id>/', mostrar_pdfRG, name='mostrar_pdfRG'),
  
   

    # Completas
    path('completas/', ComisariasCompletaRGListView.as_view(), name='comisarias_completaRG_list'),
]
