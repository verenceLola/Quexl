import asyncio
import json
from contextlib import contextmanager

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder

from quexl.utils.websocket import VerifyJSON
from quexl.utils.websocket import WebSocketAuthenticate
from quexl.utils.websockets import get_or_create_thread
from quexl.utils.websockets import save_message_to_db


class BroadcastChatConsumer(AsyncJsonWebsocketConsumer):
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
    async def receive(self, data: dict):
        to_users = data.get("to")
        message = data.get("message")
        sender = self.scope["user"]

        async def broadcast_message(
            user,
        ):  # TODO: modify function to make it idempotent for asynchronicy
            """
            broadcast message to every user
            """
            await self.channel_layer.group_send(
                self.thread_name,
                {
                    "type": "chat.message",
                    "message": json.dumps(
                        {
                            "chatId": self.thread.id,
                            "text": message,
                            "sent_at": self.msg.sent_at,
                            "sender": {
                                "username": self.msg.sender.username,
                                "email": self.msg.sender.email,
                            },
                        },
                        cls=DjangoJSONEncoder,
                    ),
                    "failed_to_send": self.failed_users,
                },
            )

        async def save_message(
            user,
        ):  # TODO: modify function to make it idempotent for asynchronicy
            """
            save each user message to db
            """
            self.failed_users = []
            try:
                user = await database_sync_to_async(
                    get_user_model().objects.get
                )(username=user["username"])
                self.thread = await get_or_create_thread(
                    self, user, "dm", [user, sender]
                )
                await self.channel_layer.group_add(
                    self.thread.name, self.channel_name
                )
                self.msg = await save_message_to_db(self, message)
            except get_user_model().DoesNotExist:
                self.failed_users.append(user)

        @contextmanager
        def processMsg(user):
            try:
                yield asyncio.create_task(save_message(user))
            finally:
                broadcast = asyncio.create_task(broadcast_message(user))
                asyncio.wait_for(broadcast, timeout=None)

        for user in to_users:
            with processMsg(user) as event:
                await event

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
