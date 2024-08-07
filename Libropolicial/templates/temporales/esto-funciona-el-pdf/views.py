from datetime import datetime
from django.http import JsonResponse, HttpResponse, HttpRequest, FileResponse  # Agregar HttpRequest aquí
from django.core.serializers import serialize
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from .models import ComisariaPrimera, ComisariaSegunda, ComisariaTercera, ComisariaCuarta, ComisariaQuinta
from .forms import ComisariaPrimeraForm, ComisariaSegundaForm, ComisariaTerceraForm, ComisariaCuartaForm, ComisariaQuintaForm, CustomLoginForm
from compartido.utils import user_is_in_group
from io import BytesIO


def generate_pdf(request, comisaria_model, filename, add_signature=False):
    buffer = generate_pdf_content(request, comisaria_model, add_signature)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response

class ComisariaPrimeraListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ComisariaPrimera
    template_name = 'comisarias/primera/comisaria_primera_list.html'
    context_object_name = 'records'

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariaprimera')

    def handle_no_permission(self):
        return redirect('no_permission')

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-fecha_hora')  # Ordenar por fecha_hora en orden descendente
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(cuarto__cuarto__icontains=search_query)
        for comisaria in queryset:
            if timezone.is_naive(comisaria.fecha_hora):
                comisaria.fecha_hora = timezone.make_aware(comisaria.fecha_hora, timezone.get_current_timezone())
            comisaria.fecha_hora = timezone.localtime(comisaria.fecha_hora)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_jefessuperiores'] = self.request.user.groups.filter(name='jefessuperiores').exists()
        context['query'] = self.request.GET.get('q', '')
        context['paginate_by'] = self.request.GET.get('paginate_by', self.paginate_by)
        return context

class ComisariaPrimeraCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ComisariaPrimera
    form_class = ComisariaPrimeraForm
    template_name = 'comisarias/primera/comisaria_primera_form.html'
    success_url = reverse_lazy('comisaria_primera_list')

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariaprimera')

    def handle_no_permission(self):
        return redirect('no_permission')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ComisariaPrimeraUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ComisariaPrimera
    form_class = ComisariaPrimeraForm
    template_name = 'comisarias/primera/comisaria_primera_form.html'
    success_url = reverse_lazy('comisaria_primera_list')

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariaprimera')

    def handle_no_permission(self):
        return redirect('no_permission')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class ComisariaSegundaListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ComisariaSegunda
    template_name = 'comisarias/segunda/comisaria_segunda_list.html'

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariasegunda')

    def handle_no_permission(self):
        return redirect('no_permission')

class ComisariaSegundaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ComisariaSegunda
    form_class = ComisariaSegundaForm
    template_name = 'comisarias/segunda/comisaria_segunda_form.html'
    success_url = reverse_lazy('comisaria_segunda_list')

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariasegunda')

    def handle_no_permission(self):
        return redirect('no_permission')

class ComisariaSegundaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ComisariaSegunda
    form_class = ComisariaSegundaForm
    template_name = 'comisarias/segunda/comisaria_segunda_form.html'
    success_url = reverse_lazy('comisaria_segunda_list')

    def test_func(self):
        return user_is_in_group(self.request.user, 'comisariasegunda')

    def handle_no_permission(self):
        return redirect('no_permission')

class ComisariaTerceraListView(LoginRequiredMixin, ListView):
    model = ComisariaTercera
    template_name = 'comisarias/tercera/comisaria_tercera_list.html'

class ComisariaTerceraCreateView(LoginRequiredMixin, CreateView):
    model = ComisariaTercera
    form_class = ComisariaTerceraForm
    template_name = 'comisarias/tercera/comisaria_tercera_form.html'
    success_url = reverse_lazy('comisaria_tercera_list')

class ComisariaCuartaListView(LoginRequiredMixin, ListView):
    model = ComisariaCuarta
    template_name = 'comisarias/cuarta/comisaria_cuarta_list.html'

class ComisariaCuartaCreateView(LoginRequiredMixin, CreateView):
    model = ComisariaCuarta
    form_class = ComisariaCuartaForm
    template_name = 'comisarias/cuarta/comisaria_cuarta_form.html'
    success_url = reverse_lazy('comisaria_cuarta_list')

class ComisariaQuintaListView(LoginRequiredMixin, ListView):
    model = ComisariaQuinta
    template_name = 'comisarias/quinta/comisaria_quinta_list.html'

class ComisariaQuintaCreateView(LoginRequiredMixin, CreateView):
    model = ComisariaQuinta
    form_class = ComisariaQuintaForm
    template_name = 'comisarias/quinta/comisaria_quinta_form.html'
    success_url = reverse_lazy('comisaria_quinta_list')

class ComisariasCompletaListView(LoginRequiredMixin, ListView):
    template_name = 'comisarias/comisarias_completa_list.html'
    context_object_name = 'comisarias'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        items_per_page = self.request.GET.get('items_per_page', 10)
        
        try:
            items_per_page = int(items_per_page)
        except ValueError:
            items_per_page = 10
        
        combined_list = []

        comisarias_primera = ComisariaPrimera.objects.select_related('cuarto').all()
        comisarias_segunda = ComisariaSegunda.objects.select_related('cuarto').all()
        comisarias_tercera = ComisariaTercera.objects.select_related('cuarto').all()
        comisarias_cuarta = ComisariaCuarta.objects.select_related('cuarto').all()
        comisarias_quinta = ComisariaQuinta.objects.select_related('cuarto').all()

        for comisaria in comisarias_primera:
            comisaria.comisaria_nombre = 'Comisaria Primera'
        for comisaria in comisarias_segunda:
            comisaria.comisaria_nombre = 'Comisaria Segunda'
        for comisaria in comisarias_tercera:
            comisaria.comisaria_nombre = 'Comisaria Tercera'
        for comisaria in comisarias_cuarta:
            comisaria.comisaria_nombre = 'Comisaria Cuarta'
        for comisaria in comisarias_quinta:
            comisaria.comisaria_nombre = 'Comisaria Quinta'

        combined_list = list(comisarias_primera) + list(comisarias_segunda) + \
                        list(comisarias_tercera) + list(comisarias_cuarta) + \
                        list(comisarias_quinta)

        if query:
            combined_list = [comisaria for comisaria in combined_list if self.query_in_comisaria(comisaria, query)]

        combined_list = sorted(combined_list, key=lambda x: x.created_at, reverse=True)

        paginator = Paginator(combined_list, items_per_page)
        page = self.request.GET.get('page')
        try:
            comisarias = paginator.page(page)
        except PageNotAnInteger:
            comisarias = paginator.page(1)
        except EmptyPage:
            comisarias = paginator.page(paginator.num_pages)

        return comisarias

    def query_in_comisaria(self, comisaria, query):
        query_lower = query.lower()
        return (
            (query_lower in comisaria.comisaria_nombre.lower() if comisaria.comisaria_nombre else False) or
            (query_lower in comisaria.cuarto.cuarto.lower() if comisaria.cuarto and comisaria.cuarto.cuarto else False) or
            (query_lower in comisaria.codigo.codigo.lower() if comisaria.codigo and comisaria.codigo.codigo else False) or
            (query_lower in comisaria.movil_patrulla.lower() if comisaria.movil_patrulla else False) or
            (query_lower in comisaria.a_cargo.lower() if comisaria.a_cargo else False) or
            (query_lower in comisaria.secundante.lower() if comisaria.secundante else False) or
            (query_lower in comisaria.lugar_codigo.lower() if comisaria.lugar_codigo else False) or
            (query_lower in comisaria.descripcion.lower() if comisaria.descripcion else False) or
            (query_lower in comisaria.instituciones_intervinientes.lower() if comisaria.instituciones_intervinientes else False) or
            (query_lower in comisaria.tareas_judiciales.lower() if comisaria.tareas_judiciales else False) or
            (query_lower in comisaria.fecha_hora.strftime('%Y-%m-%d %H:%M:%S').lower() if comisaria.fecha_hora else False)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['paginate_by'] = self.request.GET.get('items_per_page', 10)
        return context

def generate_pdf_content(request, comisaria_model, add_signature=False):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica", 8)
    y = height - 50

    now = timezone.now()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    registros = comisaria_model.objects.filter(created_at__range=(start_of_day, end_of_day))

    if not registros.exists():
        p.drawString(100, y, "No hay registros para hoy.")
    else:
        p.drawString(100, y, f"Registros de {comisaria_model._meta.verbose_name} - Hoy")
        y -= 20

        for registro in registros:
            p.drawString(50, y, f"Guardia: {registro.cuarto.cuarto if registro.cuarto else ''}")
            p.drawString(150, y, f"Código: {registro.codigo.codigo if registro.codigo else ''}")
            p.drawString(250, y, f"Móvil Patrulla: {registro.movil_patrulla if registro.movil_patrulla else ''}")
            p.drawString(350, y, f"A Cargo: {registro.a_cargo if registro.a_cargo else ''}")
            y -= 10
            p.drawString(50, y, f"Secundante: {registro.secundante if registro.secundante else ''}")
            p.drawString(150, y, f"Lugar del Código: {registro.lugar_codigo if registro.lugar_codigo else ''}")
            p.drawString(250, y, f"Descripción: {registro.descripcion if registro.descripcion else ''}")
            y -= 10
            p.drawString(50, y, f"Instituciones Intervinientes: {registro.instituciones_intervinientes if registro.instituciones_intervinientes else ''}")
            p.drawString(150, y, f"Tareas Judiciales: {registro.tareas_judiciales if registro.tareas_judiciales else ''}")
            y -= 20
            if y < 100:
                p.showPage()
                p.setFont("Helvetica", 8)
                y = height - 30

    if add_signature:
        username = request.user.username
        p.setFont("Helvetica-Bold", 14)
        p.setFillColorRGB(0.5, 0.5, 0.5, alpha=0.5)
        p.drawString(100, 50, f"Firmado electrónicamente por: {username}")

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

def generate_pdf(request, comisaria_model, filename, add_signature=False):
    buffer = generate_pdf_content(request, comisaria_model, add_signature)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response

def view_pdf(request, comisaria_model, template_name):
    return render(request, template_name, {'model_name': comisaria_model._meta.model_name})

def view_pdf_content(request, comisaria_model):
    buffer = generate_pdf_content(request, comisaria_model)
    response = FileResponse(buffer, content_type='application/pdf')
    return response

def generate_comisaria_primera_pdf_view(request):
    return view_pdf_content(request, ComisariaPrimera)

def generate_comisaria_primera_pdf_download(request):
    add_signature = 'signature' in request.GET
    return generate_pdf(request, ComisariaPrimera, 'comisaria_primera_registros.pdf', add_signature=add_signature)

def generate_comisaria_segunda_pdf_view(request):
    return view_pdf_content(request, ComisariaSegunda)

def generate_comisaria_segunda_pdf_download(request):
    add_signature = 'signature' in request.GET
    return generate_pdf(request, ComisariaSegunda, 'comisaria_segunda_registros.pdf', add_signature=add_signature)

def generate_comisaria_tercera_pdf_view(request):
    return view_pdf_content(request, ComisariaTercera)

def generate_comisaria_tercera_pdf_download(request):
    add_signature = 'signature' in request.GET
    return generate_pdf(request, ComisariaTercera, 'comisaria_tercera_registros.pdf', add_signature=add_signature)

def generate_comisaria_cuarta_pdf_view(request):
    return view_pdf_content(request, ComisariaCuarta)

def generate_comisaria_cuarta_pdf_download(request):
    add_signature = 'signature' in request.GET
    return generate_pdf(request, ComisariaCuarta, 'comisaria_cuarta_registros.pdf', add_signature=add_signature)

def generate_comisaria_quinta_pdf_view(request):
    return view_pdf_content(request, ComisariaQuinta)

def generate_comisaria_quinta_pdf_download(request):
    add_signature = 'signature' in request.GET
    return generate_pdf(request, ComisariaQuinta, 'comisaria_quinta_registros.pdf', add_signature=add_signature)