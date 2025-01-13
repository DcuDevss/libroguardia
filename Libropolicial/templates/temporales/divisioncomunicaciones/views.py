from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import DivisionComunicaciones, EncargadoGuardia, PersonalGuardia, EventoGuardia
from .forms import DivisionComunicacionesForm, EventoGuardiaFormSet, EventoGuardiaBisFormSet, EventoGuardiaBisUnoFormSet

# Vista de la lista
class DivisionComunicacionesListView(ListView):
    model = DivisionComunicaciones
    template_name = 'divisioncomunicaciones/divisioncomunicaciones_list.html'

    def test_func(self):
        return self.request.user.groups.filter(name='divisioncomunicaciones').exists()

    def handle_no_permission(self):
        return redirect('no_permission')


class DivisionComunicacionesCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = DivisionComunicaciones
    form_class = DivisionComunicacionesForm
    template_name = 'divisioncomunicaciones/divisioncomunicaciones_form.html'
    success_url = reverse_lazy('divisioncomunicaciones_list')

    def test_func(self):
        return self.request.user.groups.filter(name='divisioncomunicaciones').exists()

    def handle_no_permission(self):
        return redirect('no_permission')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['eventos_formset'] = EventoGuardiaFormSet(self.request.POST)
            data['eventos_bis_formset'] = EventoGuardiaBisFormSet(self.request.POST)
            data['eventos_bis_uno_formset'] = EventoGuardiaBisUnoFormSet(self.request.POST)
        else:
            data['eventos_formset'] = EventoGuardiaFormSet()
            data['eventos_bis_formset'] = EventoGuardiaBisFormSet()
            data['eventos_bis_uno_formset'] = EventoGuardiaBisUnoFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        eventos_formset = context['eventos_formset']
        eventos_bis_formset = context['eventos_bis_formset']
        eventos_bis_uno_formset = context['eventos_bis_uno_formset']

        # Guardar el formulario principal
        self.object = form.save()

        # Asignar la guardia a los formsets
        eventos_formset.instance = self.object
        eventos_bis_formset.instance = self.object
        eventos_bis_uno_formset.instance = self.object

        # Validar y guardar todos los formsets
        if (eventos_formset.is_valid() and
            eventos_bis_formset.is_valid() and
            eventos_bis_uno_formset.is_valid()):

            eventos_formset.save()
            eventos_bis_formset.save()
            eventos_bis_uno_formset.save()

            messages.success(self.request, 'Guardia y eventos guardados correctamente.')
            return redirect(self.success_url)
        else:
            # Imprimir los errores en la consola para depurar
            print(eventos_formset.errors, eventos_bis_formset.errors, eventos_bis_uno_formset.errors)
            return self.form_invalid(form)


class DivisionComunicacionesUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = DivisionComunicaciones
    form_class = DivisionComunicacionesForm
    template_name = 'divisioncomunicaciones/divisioncomunicaciones_form.html'
    success_url = reverse_lazy('divisioncomunicaciones_list')

    def test_func(self):
        return self.request.user.groups.filter(name='divisioncomunicaciones').exists()

    def handle_no_permission(self):
        return redirect('no_permission')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['eventos_formset'] = EventoGuardiaFormSet(self.request.POST, instance=self.object)
            data['eventos_bis_formset'] = EventoGuardiaBisFormSet(self.request.POST, instance=self.object)
            data['eventos_bis_uno_formset'] = EventoGuardiaBisUnoFormSet(self.request.POST, instance=self.object)
        else:
            data['eventos_formset'] = EventoGuardiaFormSet(instance=self.object)
            data['eventos_bis_formset'] = EventoGuardiaBisFormSet(instance=self.object)
            data['eventos_bis_uno_formset'] = EventoGuardiaBisUnoFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        eventos_formset = context['eventos_formset']
        eventos_bis_formset = context['eventos_bis_formset']
        eventos_bis_uno_formset = context['eventos_bis_uno_formset']

        self.object = form.save()

        eventos_formset.instance = self.object
        eventos_bis_formset.instance = self.object
        eventos_bis_uno_formset.instance = self.object

        if (eventos_formset.is_valid() and
            eventos_bis_formset.is_valid() and
            eventos_bis_uno_formset.is_valid()):
            eventos_formset.save()
            eventos_bis_formset.save()
            eventos_bis_uno_formset.save()
            messages.success(self.request, 'Guardia y eventos actualizados correctamente.')
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)


from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

# Vista para listar los usuarios de la división
class DivisionUsuariosListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'divisioncomunicaciones/usuarios_list.html'

    def get_queryset(self):
        # Filtrar por usuarios que pertenecen al grupo 'divisioncomunicaciones'
        return User.objects.filter(groups__name='divisioncomunicaciones')

    def test_func(self):
        # Verificar si el usuario tiene permiso de administración en esta dependencia
        return self.request.user.groups.filter(name='admin_divisioncomunicaciones').exists()

# Vista para crear un nuevo usuario en la división
class DivisionUsuarioCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'divisioncomunicaciones/usuario_form.html'
    success_url = reverse_lazy('division_usuarios_list')
    action = 'Crear'

    def form_valid(self, form):
        user = form.save()
        # Asignar al nuevo usuario al grupo 'divisioncomunicaciones'
        group = get_object_or_404(Group, name='divisioncomunicaciones')
        user.groups.add(group)
        messages.success(self.request, 'Usuario creado exitosamente.')
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.groups.filter(name='admin_divisioncomunicaciones').exists()

# Vista para editar un usuario de la división
class DivisionUsuarioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = 'divisioncomunicaciones/usuario_form.html'
    success_url = reverse_lazy('division_usuarios_list')
    action = 'Editar'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Editar'
        return context

    def test_func(self):
        return self.request.user.groups.filter(name='admin_divisioncomunicaciones').exists()
