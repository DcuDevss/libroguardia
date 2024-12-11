def global_user_permissions(request):
    """Agrega permisos globales al contexto de las plantillas."""
    user = request.user

    # Verificar si el usuario está autenticado
    if not user.is_authenticated:
        return {
            'can_access_comisariasRG': False,
            'can_access_comisarias': False,  
        }

    # Evaluar condiciones para los permisos
    can_access_comisariasRG = (
        user.is_superuser or 
        user.groups.filter(name='dcu101RG').exists()
    )
    can_access_comisarias = (
        user.is_staff or
        user.groups.filter(name='dcu101').exists()
    )

    # Retornar ambos permisos
    return {
        'can_access_comisariasRG': can_access_comisariasRG,
        'can_access_comisarias': can_access_comisarias,
    }
