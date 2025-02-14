#compartidos/views
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .forms import CustomLoginForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from compartido.models import Personal
from django.contrib import messages
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from .models import OTP
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import OTP
from django.utils.timezone import now
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import PasswordResetConfirmView

def no_permission(request):
    return render(request, 'no_permission.html', {})

class HomeView(TemplateView):
    template_name = 'home.html'

class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = CustomLoginForm
    

    def get_success_url(self):
        user_group_redirects = {
            'comisariaprimera': 'comisaria_primera_list',
            'comisariasegunda': 'comisaria_segunda_list',
            'comisaria_primeraRG': 'comisariaprimeraRG_list',
            'comisaria_segundaRG': 'comisariasegundaRG_list',
            'comisaria_terceraRG': 'comisariaterceraRG_list',
            'comisaria_cuartaRG': 'comisariacuartaRG_list',
            'comisaria_quintaRG': 'comisariaquintaRG_list',
            #'comisaria_tolhuin': 'comisaria_tolhuin_list', esta comentado por el modemnto
            #'divisioncomunicaciones': 'divisioncomunicaciones_list'
        }
        for group, url in user_group_redirects.items():
            if self.request.user.groups.filter(name=group).exists():
                return reverse_lazy(url)
        return reverse_lazy('no_permission')


@login_required
def perfil_usuario(request):
    # Obtener o crear el perfil personalizado del usuario autenticado
    personal_profile, created = Personal.objects.get_or_create(user=request.user)

    if created:
        # Si se creó un nuevo perfil, puedes inicializar campos predeterminados aquí si es necesario
        messages.info(request, "Se ha creado automáticamente un perfil para tu usuario.")
    
    return render(request, 'perfil_usuario.html', {'user': request.user, 'personal_profile': personal_profile})


@login_required
def actualizar_perfil(request):
    try:
        personal = request.user.personal_profile
    except Personal.DoesNotExist:
        # Crear un perfil si no existe
        personal = Personal.objects.create(user=request.user)

    # Verificar si los campos ya fueron completados
    if personal.campos_completados:
        messages.info(request, "Ya has completado tu perfil. Contacta al administrador para realizar cambios.")
        return redirect('perfil_usuario')  # Redirige si los campos ya están completados


    if request.method == 'POST':
        personal = request.user.personal_profile  # Obtiene el perfil relacionado con el usuario
        dni = request.POST.get('dni')
        legajo = request.POST.get('legajo')
        telefono = request.POST.get('telefono')
        domicilio = request.POST.get('domicilio')
        photo = request.FILES.get('photo')  # Obtiene la imagen si se sube una

        # Actualiza los campos del perfil
        personal.dni = dni
        personal.legajo = legajo
        personal.telefono = telefono
        personal.domicilio = domicilio

        if photo:
            # Abrir la imagen subida
            img = Image.open(photo)

            # Redimensionar la imagen
            max_size = (150, 150)
            img.thumbnail(max_size)

            # Guardar la imagen redimensionada en un buffer
            buffer = BytesIO()
            img_format = 'JPEG' if img.format.lower() != 'png' else 'PNG'
            img.save(buffer, format=img_format, quality=85)
            buffer.seek(0)

            # Reemplazar la imagen original por la procesada
            photo_resized = ContentFile(buffer.read(), name=photo.name)
            personal.photo = photo_resized

        personal.campos_completados = True  # Marca como completados
        personal.save()

        messages.success(request, "Perfil actualizado exitosamente.")
        return redirect('perfil_usuario')  # Redirige al perfil después de guardar
    else:
        messages.error(request, "Error al procesar la solicitud.")
        return redirect('perfil_usuario')
    
@csrf_exempt
@login_required
def cambiar_contrasena(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantiene la sesión activa tras el cambio de contraseña
            return JsonResponse({'success': True, 'message': 'Contraseña actualizada correctamente.'})
        else:
            # Envía errores detallados al cliente
            errors = {field: [error['message'] for error in error_list] for field, error_list in form.errors.get_json_data().items()}
            return JsonResponse({'success': False, 'errors': errors})
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)


User = get_user_model()

class CustomPasswordResetView(PasswordResetView):
    email_template_name = "registration/password_reset_email.html"  # Esta plantilla se usará para enviar el OTP
    subject_template_name = "registration/custom_password_reset_subject.txt"
    html_email_template_name = "registration/password_reset_email.html"
    success_url = reverse_lazy("verificar_otp")  # Cambia el éxito para redirigir a la vista de validación OTP

    def form_valid(self, form):
        # Buscar al usuario por correo electrónico
        email = form.cleaned_data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Si el usuario no existe, ignora el error por seguridad
            return super().form_valid(form)

        # Crear o actualizar el OTP para el usuario
        otp, created = OTP.objects.get_or_create(user=user)
        otp.generate_code()

        # Enviar el correo con el OTP
        context = {
            "otp": otp.code,
            "user": user,
            "protocol": self.request.scheme,
            "domain": self.request.get_host(),
        }
        self.send_otp_email(user.email, context)

        # Almacenar el usuario en la sesión temporalmente para validar el OTP
        self.request.session["reset_user_id"] = user.pk
        return redirect(self.success_url)

    def send_otp_email(self, email, context):
        # Asegúrate de que el contexto es un diccionario
        if not isinstance(context, dict):
            raise TypeError("context must be a dict rather than str.")

        subject = "Código de Verificación para Restablecimiento de Contraseña"
        message = render_to_string('otp_email.html', context)  # Renderiza el contenido del correo con la plantilla
        send_mail(
            subject,
            '',  # El cuerpo de texto plano se deja vacío para usar el formato HTML
            "no-reply@example.com",
            [email],
            html_message=message  # Agrega el HTML como mensaje principal
        )


def verificar_otp(request):
    user_id = request.session.get("reset_user_id")
    if not user_id:
        messages.error(request, "No se ha iniciado un proceso de restablecimiento de contraseña.")
        return redirect("password_reset")

    if request.method == "POST":
        otp_code = request.POST.get("otp")
        try:
            otp = OTP.objects.get(user_id=user_id, code=otp_code, is_valid=True)
            if (now() - otp.created_at).total_seconds() > 300:  # Expira en 5 minutos
                otp.invalidate()
                messages.error(request, "El código OTP ha expirado.")
                return redirect("password_reset")
            
            otp.invalidate()
            
            # Redirigir al PasswordResetConfirmView con uidb64 y token
            user = User.objects.get(pk=user_id)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            return redirect("password_reset_confirm", uidb64=uidb64, token=token)
        except OTP.DoesNotExist:
            messages.error(request, "El código OTP ingresado es incorrecto.")
            return redirect("verificar_otp")

    return render(request, "registration/verificar_otp.html")


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'  # El template que usarás
    success_url = reverse_lazy('password_reset_complete')  # Redirección tras éxito

    def form_valid(self, form):
        # Cambiar la contraseña y mostrar un mensaje de éxito
        response = super().form_valid(form)
        messages.success(self.request, "¡Tu contraseña ha sido cambiada exitosamente!")
        return response

    def form_invalid(self, form):
        # Manejar errores en el formulario
        messages.error(self.request, "Hubo un error al cambiar la contraseña. Revisa los datos ingresados.")
        return super().form_invalid(form)