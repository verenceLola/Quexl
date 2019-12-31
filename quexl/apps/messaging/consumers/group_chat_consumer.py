import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core.serializers.json import DjangoJSONEncoder

from quexl.apps.messaging.models import Thread
from quexl.utils.websocket import VerifyJSON
from quexl.utils.websocket import WebSocketAuthenticate
from quexl.utils.websockets import save_message_to_db


class GroupChatConsumer(AsyncJsonWebsocketConsumer):
    @WebSocketAuthenticate()
    async def connect(self):
        """
        establish websocket connection
        """
        await self.send_json({"message": "connection established"})

    async def disconnect(self, close_code):
        """
        close websocket connection
        """
        await self.channel_layer.group_discard(
            getattr(self, "group_name", "no-name"), self.channel_name
        )

    @VerifyJSON()
    async def receive(self, json_data):
        """
        process recieved text
        """
        self.thread_name = json_data.get("group")
        message = json_data.get("message")
        self.group_name = f"{self.thread_name}"
        try:
            self.thread = await database_sync_to_async(Thread.objects.get)(
                name=self.group_name
            )
            if not Thread.objects.filter(
                participants__in=[self.scope["user"]]
            ).exists():
                await self.send_json(
                    {
                        "error": f"Message not sent. You're not a member of this group"
                    }
                )
                return
        except Thread.DoesNotExist:
            await self.send_json(
                {
                    "error": f"Message not sent. Group named"
                    " '{self.group_name}' doesn't exist"
                }
            )
            return
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        msg = await save_message_to_db(self, message)
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.message",
                "message": json.dumps(
                    {
                        "chatId": self.thread.id,
                        "text": message,
                        "sent_at": msg.sent_at,
                        "sender": {
                            "username": msg.sender.username,
                            "email": msg.sender.email,
                        },
                    },
                    cls=DjangoJSONEncoder,
                ),
            },
        )

    async def chat_message(self, event):
        message = {"message": json.loads(event["message"])}
        await self.send_json(message)
