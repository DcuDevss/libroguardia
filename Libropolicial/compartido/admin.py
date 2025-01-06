from django.contrib import admin
from .models import CodigoPolicialUSH, CodigosSecundarios, CuartoGuardiaUSH
from .models import CodigoPolicialRG, CodigosSecundariosRG, CuartoGuardiaRG
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import Personal
from django.core.exceptions import ValidationError

# Register your models here.
# Admin para CuartoGuardiaUSH con opción de activar/desactivar-
@admin.register(CuartoGuardiaUSH)
class CuartoGuardiaUSHAdmin(admin.ModelAdmin):
    list_display = ('cuarto', 'activo')  # Mostrar si está activo o no
    search_fields = ('cuarto',)
    list_filter = ('activo',)  # Agregar filtro por activos

# Admin para CodigoPolicialUSH con opción de activar/desactivar
@admin.register(CodigoPolicialUSH)
class CodigoPolicialUSHAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'activo')  # Mostrar si está activo o no
    search_fields = ('codigo',)
    list_filter = ('activo',)  # Agregar filtro por activos

# Admin para CodigosSecundarios con opción de activar/desactivar
@admin.register(CodigosSecundarios)
class CodigosSecundariosAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'activo')  # Mostrar si está activo o no
    search_fields = ('codigo',)
    list_filter = ('activo',)  # Agregar filtro por activos



#*******************ADMIN PARA RG**********************    

# Admin para CuartoGuardiaRG con opción de activar/desactivar
@admin.register(CuartoGuardiaRG)
class CuartoGuardiaRGAdmin(admin.ModelAdmin):
    list_display = ('cuartoRG', 'activo')  # Mostrar si está activo o no
    search_fields = ('cuartoRG',)
    list_filter = ('activo',)  # Agregar filtro por activos

# Admin para CodigoPolicialUSH con opción de activar/desactivar
@admin.register(CodigoPolicialRG)
class CodigoPolicialRGAdmin(admin.ModelAdmin):
    list_display = ('codigoRG', 'activo')  # Mostrar si está activo o no
    search_fields = ('codigoRG',)
    list_filter = ('activo',)  # Agregar filtro por activos

# Admin para CodigosSecundarios con opción de activar/desactivar
@admin.register(CodigosSecundariosRG)
class CodigosSecundariosRGAdmin(admin.ModelAdmin):
    list_display = ('codigoRG', 'activo')  # Mostrar si está activo o no
    search_fields = ('codigoRG',)
    list_filter = ('activo',)  # Agregar filtro por activos    


#*******************ADMIN**********************    
User = get_user_model()
# Define un inline admin para el modelo Personal
class PersonalInline(admin.StackedInline):
    model = Personal
    can_delete = False
    verbose_name_plural = "Perfil Personal"
    fields = ('legajo', 'dni')  # Campos que el superadmin puede editar


# Personaliza la administración del usuario para incluir el perfil
class CustomUserAdmin(BaseUserAdmin):
    inlines = (PersonalInline,)  # Agrega los campos del modelo Personal en el panel de usuarios
    list_display = ('username', 'email', 'is_staff', 'is_superuser')  # Muestra los campos principales en la lista
    search_fields = ('username', 'email', 'personal_profile__legajo', 'personal_profile__dni')  # Permite búsquedas avanzadas
    list_filter = ('is_staff', 'is_superuser', 'is_active')

    # Campos que aparecerán al editar/crear un usuario
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

    # Campos que aparecerán al crear un usuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    def save_model(self, request, obj, form, change):
        # Guardar el usuario primero
        obj.save()

        # Validar unicidad del correo electrónico
        if User.objects.filter(email=obj.email).exclude(pk=obj.pk).exists():
            raise ValidationError(f"El correo electrónico {obj.email} ya está en uso.")


        # Validar unicidad del legajo y dni
        if hasattr(obj, 'personal_profile'):
            personal_profile = obj.personal_profile
            if personal_profile.legajo and Personal.objects.filter(legajo=personal_profile.legajo).exclude(user=obj).exists():
                raise ValidationError(f"El legajo {personal_profile.legajo} ya está en uso.")
            if personal_profile.dni and Personal.objects.filter(dni=personal_profile.dni).exclude(user=obj).exists():
                raise ValidationError(f"El DNI {personal_profile.dni} ya está en uso.")
        
        super().save_model(request, obj, form, change)



# Registra el modelo de usuario personalizado
admin.site.unregister(User)  # Desregistra el modelo User predeterminado
admin.site.register(User, CustomUserAdmin)  # Registra el modelo User con el nuevo admin