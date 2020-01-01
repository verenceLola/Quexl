from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from quexl.apps.messaging.models import Message


class SaveMessage:
    """
    save message to db
    """

    @staticmethod
    @database_sync_to_async
    def __call__(self: AsyncJsonWebsocketConsumer, text: str) -> Message:
        """"
        save message to db
        """
        sender = self.scope["user"]
        msg = Message.objects.create(
            sender=sender, text=text, thread=self.thread
        )
        return msg
