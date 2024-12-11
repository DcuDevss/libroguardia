from django.urls import path
from .views import (
    # Funciones para generar PDFs y firmas
    generate_comisaria_primera_pdf_view, generate_comisaria_primera_pdf_download,
    generate_comisaria_segunda_pdf_view, generate_comisaria_segunda_pdf_download,
    generate_comisaria_tercera_pdf_view, generate_comisaria_tercera_pdf_download,
    generate_comisaria_cuarta_pdf_view, generate_comisaria_cuarta_pdf_download,
    generate_comisaria_quinta_pdf_view, generate_comisaria_quinta_pdf_download,
    generate_comisaria_primera_pdf_download_previous_day, generate_comisaria_segunda_pdf_download_previous_day,
    generate_comisaria_tercera_pdf_download_previous_day, generate_comisaria_cuarta_pdf_download_previous_day,
    generate_comisaria_quinta_pdf_download_previous_day,
    sign_comisaria_primera, sign_comisaria_segunda, sign_comisaria_tercera, sign_comisaria_cuarta, sign_comisaria_quinta,
    
    # Otras funciones y vistas
    subir_pdf, ver_pdfs, mostrar_pdf, generar_mapa, estadisticas_comisarias,
    
    # Vistas de listas y CRUD de comisarías
    ComisariaPrimeraListView, ComisariaSegundaListView, ComisariaTerceraListView,
    ComisariaCuartaListView, ComisariaQuintaListView, ComisariasCompletaListView,
    
    # Vistas de creación
    ComisariaPrimeraCreateView, ComisariaSegundaCreateView, ComisariaTerceraCreateView,
    ComisariaCuartaCreateView, ComisariaQuintaCreateView,
    
    # Vistas de actualización
    ComisariaPrimeraUpdateView, ComisariaSegundaUpdateView, ComisariaTerceraUpdateView,
    ComisariaCuartaUpdateView, ComisariaQuintaUpdateView,
    
    # Vistas de detalle
    ComisariaPrimeraDetailView, ComisariaSegundaDetailView, ComisariaTerceraDetailView,
    ComisariaCuartaDetailView, ComisariaQuintaDetailView,

     #softdelete
    eliminar_comisaria_primera, eliminar_comisaria_segunda, eliminar_comisaria_tercera, eliminar_comisaria_cuarta,
    eliminar_comisaria_quinta
)

urlpatterns = [
    # Comisaría Primera
    path('primera/', ComisariaPrimeraListView.as_view(), name='comisaria_primera_list'),
    path('primera/create/', ComisariaPrimeraCreateView.as_view(), name='comisaria_primera_create'),
    path('primera/edit/<int:pk>/', ComisariaPrimeraUpdateView.as_view(), name='comisaria_primera_edit'),
    path('comisarias/primera/detalle/<int:pk>/', ComisariaPrimeraDetailView.as_view(), name='comisaria_primera_detail'),
    path('primera/reporte/view/', generate_comisaria_primera_pdf_view, name='generate_comisaria_primera_pdf_view'),
    path('primera/reporte/download/', generate_comisaria_primera_pdf_download, name='generate_comisaria_primera_pdf_download'),
    path('comisarias/primera/descargar-dia-anterior/', generate_comisaria_primera_pdf_download_previous_day, name='generate_comisaria_primera_pdf_download_previous_day'),
    path('primera/firmar/<int:pk>/', sign_comisaria_primera, name='comisaria_primera_sign'),
    path('primera/eliminar/<int:pk>/', eliminar_comisaria_primera, name='comisaria_primera_eliminar'),


    # Comisaría Segunda
    path('segunda/', ComisariaSegundaListView.as_view(), name='comisaria_segunda_list'),
    path('segunda/nuevo/', ComisariaSegundaCreateView.as_view(), name='comisaria_segunda_create'),
    path('segunda/editar/<int:pk>/', ComisariaSegundaUpdateView.as_view(), name='comisaria_segunda_edit'),
    path('comisarias/segunda/detalle/<int:pk>/', ComisariaSegundaDetailView.as_view(), name='comisaria_segunda_detail'),
    path('segunda/reporte/', generate_comisaria_segunda_pdf_view, name='generate_comisaria_segunda_pdf_view'),
    path('segunda/reporte/download/', generate_comisaria_segunda_pdf_download, name='generate_comisaria_segunda_pdf_download'),
    path('comisarias/segunda/descargar-dia-anterior/', generate_comisaria_segunda_pdf_download_previous_day, name='generate_comisaria_segunda_pdf_download_previous_day'),
    path('segunda/firmar/<int:pk>/', sign_comisaria_segunda, name='comisaria_segunda_sign'),
    path('segunda/eliminar/<int:pk>/', eliminar_comisaria_segunda, name='comisaria_segunda_eliminar'),

    # Comisaría Tercera
    path('tercera/', ComisariaTerceraListView.as_view(), name='comisaria_tercera_list'),
    path('tercera/nuevo/', ComisariaTerceraCreateView.as_view(), name='comisaria_tercera_create'),
    path('tercera/editar/<int:pk>/', ComisariaTerceraUpdateView.as_view(), name='comisaria_tercera_edit'),
    path('comisarias/tercera/detalle/<int:pk>/', ComisariaTerceraDetailView.as_view(), name='comisaria_tercera_detail'),
    path('tercera/reporte/', generate_comisaria_tercera_pdf_view, name='generate_comisaria_tercera_pdf_view'),
    path('tercera/reporte/download/', generate_comisaria_tercera_pdf_download, name='generate_comisaria_tercera_pdf_download'),
    path('comisarias/tercera/descargar-dia-anterior/', generate_comisaria_tercera_pdf_download_previous_day, name='generate_comisaria_tercera_pdf_download_previous_day'),
    path('tercera/firmar/<int:pk>/', sign_comisaria_tercera, name='comisaria_tercera_sign'),
    path('tercera/eliminar/<int:pk>/', eliminar_comisaria_tercera, name='comisaria_tercera_eliminar'),

    # Comisaría Cuarta
    path('cuarta/', ComisariaCuartaListView.as_view(), name='comisaria_cuarta_list'),
    path('cuarta/nuevo/', ComisariaCuartaCreateView.as_view(), name='comisaria_cuarta_create'),
    path('cuarta/editar/<int:pk>/', ComisariaCuartaUpdateView.as_view(), name='comisaria_cuarta_edit'),
    path('comisarias/cuarta/detalle/<int:pk>/', ComisariaCuartaDetailView.as_view(), name='comisaria_cuarta_detail'),
    path('cuarta/reporte/', generate_comisaria_cuarta_pdf_view, name='generate_comisaria_cuarta_pdf_view'),
    path('cuarta/reporte/download/', generate_comisaria_cuarta_pdf_download, name='generate_comisaria_cuarta_pdf_download'),
    path('comisarias/cuarta/descargar-dia-anterior/', generate_comisaria_cuarta_pdf_download_previous_day, name='generate_comisaria_cuarta_pdf_download_previous_day'),
    path('cuarta/firmar/<int:pk>/', sign_comisaria_cuarta, name='comisaria_cuarta_sign'),
    path('cuarta/eliminar/<int:pk>/', eliminar_comisaria_cuarta, name='comisaria_cuarta_eliminar'),


    # Comisaría Quinta
    path('quinta/', ComisariaQuintaListView.as_view(), name='comisaria_quinta_list'),
    path('quinta/nuevo/', ComisariaQuintaCreateView.as_view(), name='comisaria_quinta_create'),
    path('quinta/editar/<int:pk>/', ComisariaQuintaUpdateView.as_view(), name='comisaria_quinta_edit'),
    path('comisarias/quinta/detalle/<int:pk>/', ComisariaQuintaDetailView.as_view(), name='comisaria_quinta_detail'),
    path('quinta/reporte/', generate_comisaria_quinta_pdf_view, name='generate_comisaria_quinta_pdf_view'),
    path('quinta/reporte/download/', generate_comisaria_quinta_pdf_download, name='generate_comisaria_quinta_pdf_download'),
    path('comisarias/quinta/descargar-dia-anterior/', generate_comisaria_quinta_pdf_download_previous_day, name='generate_comisaria_quinta_pdf_download_previous_day'),
    path('quinta/firmar/<int:pk>/', sign_comisaria_quinta, name='comisaria_quinta_sign'),
    path('quinta/eliminar/<int:pk>/', eliminar_comisaria_quinta, name='comisaria_quinta_eliminar'),


    # Otras rutas
    path('subir-pdf/', subir_pdf, name='subir_pdf'),
    path('ver-pdfs/', ver_pdfs, name='ver_pdfs'),  # Nueva URL para ver los PDFs
    path('mostrar-pdf/<int:pdf_id>/', mostrar_pdf, name='mostrar_pdf'),
    path('mapa/', generar_mapa, name='generar_mapa'),
    path('estadisticas/', estadisticas_comisarias, name='estadisticas_comisarias'),

    # Completas
    path('completas/', ComisariasCompletaListView.as_view(), name='comisarias_completa_list'),
]
