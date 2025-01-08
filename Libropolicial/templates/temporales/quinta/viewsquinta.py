#--------------------vista dee todas las comisarias-------------------------------------    

from django.db.models import Value, Q, CharField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class ComisariasCompletaListView(LoginRequiredMixin, ListView):
    template_name = 'comisarias/comisarias_completa_list.html'
    context_object_name = 'page_obj'

    def get_paginate_by(self, queryset):
        """Define el número de registros por página dinámicamente."""
        items_per_page = self.request.GET.get('items_per_page', 10)
        try:
            return int(items_per_page)
        except ValueError:
            return 10  # Valor por defecto si no es válido

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()  # Obtiene y limpia la consulta

        # Crea un filtro Q común para reutilizarlo
        search_filter = (
            Q(comisaria_nombre__icontains=query) |
            Q(cuarto__cuarto__icontains=query) |
            Q(codigo__codigo__icontains=query) |
            Q(codigo__nombre_codigo__icontains=query) |
            Q(movil_patrulla__icontains=query) |
            Q(a_cargo__icontains=query) |
            Q(secundante__icontains=query) |
            Q(lugar_codigo__icontains=query) |
            Q(tareas_judiciales__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(fecha_hora__icontains=query)
        ) if query else Q()  # Solo aplica el filtro si hay una consulta

        # Filtra y anota cada QuerySet individualmente
        comisarias_primera = ComisariaPrimera.objects.filter(
            activo=True
        ).select_related('cuarto').annotate(
            comisaria_nombre=Value('Comisaria Primera', output_field=CharField())
        ).filter(search_filter)

        comisarias_segunda = ComisariaSegunda.objects.filter(
            activo=True
        ).select_related('cuarto').annotate(
            comisaria_nombre=Value('Comisaria Segunda', output_field=CharField())
        ).filter(search_filter)

        comisarias_tercera = ComisariaTercera.objects.filter(
            activo=True
        ).select_related('cuarto').annotate(
            comisaria_nombre=Value('Comisaria Tercera', output_field=CharField())
        ).filter(search_filter)

        comisarias_cuarta = ComisariaCuarta.objects.filter(
            activo=True
        ).select_related('cuarto').annotate(
            comisaria_nombre=Value('Comisaria Cuarta', output_field=CharField())
        ).filter(search_filter)

        comisarias_quinta = ComisariaQuinta.objects.filter(
            activo=True
        ).select_related('cuarto').annotate(
            comisaria_nombre=Value('Comisaria Quinta', output_field=CharField())
        ).filter(search_filter)

        # Unión de los QuerySets
        combined_queryset = comisarias_primera.union(
            comisarias_segunda,
            comisarias_tercera,
            comisarias_cuarta,
            comisarias_quinta
        )

        # Ordenar por fecha de creación
        return combined_queryset.order_by('-created_at')
    
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

    # Paginación
        paginate_by = self.get_paginate_by(queryset)
        paginator = Paginator(queryset, paginate_by)
        page = self.request.GET.get('page')

        try:
           page_obj = paginator.page(page)
        except PageNotAnInteger:
           page_obj = paginator.page(1)
        except EmptyPage:
           page_obj = paginator.page(paginator.num_pages)

    # Calcular el rango dinámico de páginas
        current_page = page_obj.number
        total_pages = page_obj.paginator.num_pages
        range_start = max(current_page - 5, 1)
        range_end = min(current_page + 5, total_pages) + 1  # Incluye la última página

        context['page_obj'] = page_obj
        context['query'] = self.request.GET.get('q', '')
        context['items_per_page'] = paginate_by
        context['page_range'] = range(range_start, range_end)
        return context

