# compartido/utils.py
def user_is_in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


from django.http import JsonResponse

def verificar_registros_activos(request, model, estado_field='estado', activo_field='activo', estado_valor=True, activo_valor=True):
    """
    Verifica si hay registros activos en el modelo dado.

    :param model: El modelo de Django a verificar.
    :param estado_field: El nombre del campo de estado en el modelo.
    :param activo_field: El nombre del campo de activo en el modelo.
    :param estado_valor: El valor esperado del campo de estado para considerarlo activo.
    :param activo_valor: El valor esperado del campo de activo para considerarlo activo.
    :return: JsonResponse si hay registros activos, None si no hay problemas.
    """
    # Verifica si se debe forzar la descarga
    force_download = request.GET.get('force', 'false').lower() == 'true'

    # Filtra registros que cumplan con los criterios de estado y activo.
    filtro = {estado_field: estado_valor, activo_field: activo_valor}
    registros_activos = model.objects.filter(**filtro).exists()

    if registros_activos and not force_download:
        # Si la solicitud es AJAX, retorna un JSON con advertencia
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'warning': f'Existen registros con el estado "Activo" en {model._meta.verbose_name}. ¿Deseas continuar con la descarga del PDF?'
            })
        
    return None