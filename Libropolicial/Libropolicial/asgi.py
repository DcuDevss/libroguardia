# libropolicial/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from compartido.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Libropolicial.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Maneja solicitudes HTTP
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns  # Aquí es donde se configuran las rutas de WebSocket
        )
    ),
})
