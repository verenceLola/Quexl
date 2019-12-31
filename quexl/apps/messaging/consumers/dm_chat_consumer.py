import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core.serializers.json import DjangoJSONEncoder

from quexl.utils.websocket import VerifyJSON
from quexl.utils.websocket import WebSocketAuthenticate
from quexl.utils.websocket import WebSocketUserExists
from quexl.utils.websockets import get_or_create_thread
from quexl.utils.websockets import save_message_to_db


class DMChatConsumer(AsyncJsonWebsocketConsumer):
    @WebSocketAuthenticate()
    async def connect(self):
        """
        establish websocket connection
        """
        await self.send_json({"message": "connection established"})

    async def disconnect(self, close_code):
        """
        close client connection
        """
        await self.channel_layer.group_discard(
            getattr(self, "group_name", "no-name"), self.channel_name
        )

    @VerifyJSON()
    @WebSocketUserExists()
    async def receive(self, json_data):
        """
        process recieved text
        """
        message = json_data.get("message")
        self.thread = await get_or_create_thread(
            self, self.to, "dm", [self.to, self.scope["user"]]
        )
        self.group_name = self.thread_name
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
