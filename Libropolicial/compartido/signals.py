from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Personal

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Crea automáticamente un perfil de Personal para cada nuevo usuario.
    """
    if created and not hasattr(instance, 'personal_profile'):
        Personal.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Guarda automáticamente el perfil de Personal cuando se actualiza el usuario.
    """
    if hasattr(instance, 'personal_profile'):
        instance.personal_profile.save()
