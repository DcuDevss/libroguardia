from django.urls import path
from .views import (
    DivisionComunicacionesListView, DivisionComunicacionesCreateView, DivisionComunicacionesUpdateView,
    DivisionUsuariosListView, DivisionUsuarioCreateView, DivisionUsuarioUpdateView
)

urlpatterns = [
    path('', DivisionComunicacionesListView.as_view(), name='divisioncomunicaciones_list'),
    path('nuevo/', DivisionComunicacionesCreateView.as_view(), name='divisioncomunicaciones_create'),
    path('<int:pk>/editar/', DivisionComunicacionesUpdateView.as_view(), name='divisioncomunicaciones_update'),
    # Rutas para la administración de usuarios
    path('usuarios/', DivisionUsuariosListView.as_view(), name='division_usuarios_list'),
    path('usuarios/nuevo/', DivisionUsuarioCreateView.as_view(), name='division_usuario_create'),
    path('usuarios/<int:pk>/editar/', DivisionUsuarioUpdateView.as_view(), name='division_usuario_update'),
]
