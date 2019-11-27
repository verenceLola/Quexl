from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from quexl.apps.messaging.models import Thread
import json
from django.core.serializers.json import DjangoJSONEncoder
from quexl.utils.websocket import get_or_create_thread, save_message_to_db
import asyncio
from contextlib import contextmanager


class DMChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        """
        establish websocket connection
        """
        if not self.scope["user"].is_authenticated:
            await self.accept()
            await self.send_json({"error": self.scope["error"]})
            await self.close()
            return

        await self.accept()
        await self.send_json({"message": "connection established"})

    async def disconnect(self, close_code):
        """
        close client connection
        """
        await self.channel_layer.group_discard(
            getattr(self, "group_name", "no-name"), self.channel_name
        )

    async def receive_json(self, json_data):
        """
        process recieved text
        """
        self.to = json_data.get("to")
        message = json_data.get("message")

        if self.to.lower() == self.scope["user"].username.lower():
            await self.accept()
            await self.send_json({"error": "You can't chat with yourself"})
            await self.close()
            return
        try:
            self.to = await database_sync_to_async(
                get_user_model().objects.get
            )(username=self.to)
        except get_user_model().DoesNotExist:
            await self.accept()
            await self.send_json(
                {"error": f"user with username '{self.to}' does not exist"}
            )
            await self.close()
            return

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


class GroupChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        """
        establish websocket connection
        """
        if not self.scope["user"].is_authenticated:
            await self.accept()
            await self.send_json({"error": self.scope["error"]})
            await self.close()
            return
        await self.accept()
        await self.send_json({"message": "connection established"})

    async def disconnect(self, close_code):
        """
        close websocket connection
        """
        await self.channel_layer.group_discard(
            getattr(self, "group_name", "no-name"), self.channel_name
        )

    async def receive_json(self, json_data):
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


class BroadcastChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        """
        establish websocket connection
        """
        if not self.scope["user"].is_authenticated:
            await self.accept()
            await self.send_json({"error": self.scope["error"]})
            await self.close()
            return
        await self.accept()
        await self.send_json({"message": "connection established"})

    async def disconnect(self, close_code):
        """
        close client connection
        """
        await self.channel_layer.group_discard(
            getattr(self, "group_name", "no-name"), self.channel_name
        )

    async def receive_json(self, data: dict):
        to_users = data.get("to")
        message = data.get("message")
        sender = self.scope["user"]

        async def broadcast_message(
            user
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
            user
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
