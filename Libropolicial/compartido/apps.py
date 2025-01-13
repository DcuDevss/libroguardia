from django.apps import AppConfig


class CompartidoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'compartido'

    def ready(self):
        import compartido.signals  # Asegúrate de que el archivo `signals.py` exista

