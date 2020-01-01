import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from quexl.utils.websocket import Authenticate
from quexl.utils.websocket import BroadCastMessage
from quexl.utils.websocket import VerifyJSON


class BroadcastChatConsumer(AsyncJsonWebsocketConsumer):
    @Authenticate()
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
    async def receive(self, data: dict):
        to_users = data.get("to")
        message = data.get("message")
        sender = self.scope["user"]
        broadcastMsg = BroadCastMessage(self, message, sender)
        await broadcastMsg(to_users)

    async def chat_message(self, event: dict):
        message = (
            {
                "message": json.loads(event["message"]),
                "errors": {
                    "users": event["failed_to_send"],
                    "message": "Failed to send message to the following users."
                    " Username(s) not found",
                },
            }
            if event.get("failed_to_send")
            else {"message": json.loads(event["message"])}
        )
        await self.send_json(message)
