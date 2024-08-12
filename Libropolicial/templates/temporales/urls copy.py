from django.urls import path
from .views import (
    generate_comisaria_primera_pdf_view, generate_comisaria_primera_pdf_download,
    generate_comisaria_segunda_pdf_view, generate_comisaria_segunda_pdf_download,
    generate_comisaria_tercera_pdf_view, generate_comisaria_tercera_pdf_download,
    generate_comisaria_cuarta_pdf_view, generate_comisaria_cuarta_pdf_download,
    generate_comisaria_quinta_pdf_view, generate_comisaria_quinta_pdf_download,
    sign_comisaria_primera, sign_comisaria_segunda,
    comisaria_primera_list, comisaria_primera_create, comisaria_primera_update,  # Cambiado a funciones
    ComisariaSegundaListView, ComisariaTerceraListView,
    ComisariaCuartaListView, ComisariaQuintaListView,
    ComisariaSegundaCreateView, ComisariaTerceraCreateView, ComisariaCuartaCreateView,
    ComisariaQuintaCreateView, ComisariasCompletaListView,
    ComisariaSegundaUpdateView, ComisariaPrimeraResolveView
)

urlpatterns = [
    path('primera/', comisaria_primera_list, name='comisaria_primera_list'),
    path('primera/create/', comisaria_primera_create, name='comisaria_primera_create'),
    path('primera/edit/<int:pk>/', comisaria_primera_update, name='comisaria_primera_edit'),
    path('primera/constancia/<int:pk>/', comisaria_primera_update, name='comisaria_primera_resolve'),
    path('primera/reporte/view/', generate_comisaria_primera_pdf_view, name='generate_comisaria_primera_pdf_view'),
    path('primera/reporte/download/', generate_comisaria_primera_pdf_download, name='generate_comisaria_primera_pdf_download'),
    path('primera/firmar/<int:pk>/', sign_comisaria_primera, name='comisaria_primera_sign'),

    path('segunda/', ComisariaSegundaListView.as_view(), name='comisaria_segunda_list'),
    path('segunda/nuevo/', ComisariaSegundaCreateView.as_view(), name='comisaria_segunda_create'),
    path('segunda/editar/<int:pk>/', ComisariaSegundaUpdateView.as_view(), name='comisaria_segunda_edit'),
    path('segunda/reporte/', generate_comisaria_segunda_pdf_view, name='generate_comisaria_segunda_pdf_view'),
    path('segunda/reporte/download/', generate_comisaria_segunda_pdf_download, name='generate_comisaria_segunda_pdf_download'),
    path('segunda/firmar/<int:pk>/', sign_comisaria_segunda, name='comisaria_segunda_sign'),

    path('tercera/', ComisariaTerceraListView.as_view(), name='comisaria_tercera_list'),
    path('tercera/nuevo/', ComisariaTerceraCreateView.as_view(), name='comisaria_tercera_create'),
    path('tercera/reporte/', generate_comisaria_tercera_pdf_view, name='generate_comisaria_tercera_pdf_view'),
    path('tercera/reporte/download/', generate_comisaria_tercera_pdf_download, name='generate_comisaria_tercera_pdf_download'),

    path('cuarta/', ComisariaCuartaListView.as_view(), name='comisaria_cuarta_list'),
    path('cuarta/nuevo/', ComisariaCuartaCreateView.as_view(), name='comisaria_cuarta_create'),
    path('cuarta/reporte/', generate_comisaria_cuarta_pdf_view, name='generate_comisaria_cuarta_pdf_view'),
    path('cuarta/reporte/download/', generate_comisaria_cuarta_pdf_download, name='generate_comisaria_cuarta_pdf_download'),

    path('quinta/', ComisariaQuintaListView.as_view(), name='comisaria_quinta_list'),
    path('quinta/nuevo/', ComisariaQuintaCreateView.as_view(), name='comisaria_quinta_create'),
    path('quinta/reporte/', generate_comisaria_quinta_pdf_view, name='generate_comisaria_quinta_pdf_view'),
    path('quinta/reporte/download/', generate_comisaria_quinta_pdf_download, name='generate_comisaria_quinta_pdf_download'),

    path('completas/', ComisariasCompletaListView.as_view(), name='comisarias_completa_list'),
]
