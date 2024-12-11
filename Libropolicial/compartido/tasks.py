# compartido/tasks.py

from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@shared_task
def send_notification(message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'notifications',  # Nombre del grupo de WebSocket
        {
            'type': 'send_message',
            'message': message
        }
    )
