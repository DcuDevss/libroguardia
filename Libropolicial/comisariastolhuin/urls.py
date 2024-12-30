# Libropolicial/comisariastolhuin/urls.py
from django.urls import path
from . import views
from .views import (
    # Funciones para generar PDFs y firmas
    generate_comisaria_tolhuin_pdf_view, generate_comisaria_tolhuin_pdf_download,
    generate_comisaria_tolhuin_pdf_download_previous_day,
    sign_comisaria_tolhuin, 
    # Otras funciones y vistas
    subir_pdfTOL, ver_pdfsTOL, mostrar_pdfTOL,
    
    # Vistas de listas y CRUD de comisarías
    ComisariaTolhuinListView,
    
    # Vistas de creación
    ComisariaTolhuinCreateView,
    # Vistas de actualización
    ComisariaTolhuinUpdateView,
    # Vistas de detalle
    ComisariaTolhuinDetailView,
     #softdelete
    eliminar_comisaria_tolhuin,
    #vista para generar pdf con rango nespecifico
    generate_pdf_custom_range_view,
    #ruta para renderizar la vista
    select_range_view_tol
)

urlpatterns = [
    # Comisaría Tolhuin
    path('tolhuin/', ComisariaTolhuinListView.as_view(), name='comisaria_tolhuin_list'),
    path('tolhuin/create/', ComisariaTolhuinCreateView.as_view(), name='comisaria_tolhuin_create'),
    path('tolhuin/edit/<int:pk>/', ComisariaTolhuinUpdateView.as_view(), name='comisaria_tolhuin_edit'),
    path('comisariastolhuin/tolhuin/detalle/<int:pk>/', ComisariaTolhuinDetailView.as_view(), name='comisaria_tolhuin_detail'),
    path('tolhuin/reporte/view/', generate_comisaria_tolhuin_pdf_view, name='generate_comisaria_tolhuin_pdf_view'),
    path('tolhuin/reporte/download/', generate_comisaria_tolhuin_pdf_download, name='generate_comisaria_tolhuin_pdf_download'),
    path('comisariastolhuin/tolhuin/descargar-dia-anterior/', generate_comisaria_tolhuin_pdf_download_previous_day, name='generate_comisaria_tolhuin_pdf_download_previous_day'),
    path('tolhuin/firmar/<int:pk>/', sign_comisaria_tolhuin, name='comisaria_tolhuin_sign'),
    path('tolhuin/eliminar/<int:pk>/', eliminar_comisaria_tolhuin, name='comisaria_tolhuin_eliminar'),


    
    # Otras rutas
    path('subir-pdfTOL/', subir_pdfTOL, name='subir_pdfTOL'),
    path('ver-pdfsTOL/', ver_pdfsTOL, name='ver_pdfsTOL'),  # Nueva URL para ver los PDFs
    path('mostrar-pdfTOL/<int:pdf_id>/', mostrar_pdfTOL, name='mostrar_pdfTOL'),
     path('seleccionar-rango-tolhuin/', select_range_view_tol, name='select_range_view_tol'),
    path('generar-pdf-rango/', generate_pdf_custom_range_view, name='generate_pdf_custom_range_view'),
   
  
   

]
