import json
from contextlib import asynccontextmanager
from typing import Dict
from typing import Union

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder

from quexl.apps.account.models import User

from .create_thread import CreateThread
from .save_message import SaveMessage


class BroadCastMessage:
    """
    factory class for broadcasting message to various users
    """

    def __init__(
        self, consumer: AsyncJsonWebsocketConsumer, message: str, sender: User
    ) -> None:
        self.consumer = consumer  # noqa
        self.message = message
        self.sender = sender
        self.FAILED_USERS = []  # save non-exisiting usernames

    async def broadcast_message(
        self, user: Dict[str, str]
    ) -> None:  # TODO: Fix multiple broadcasts to sender
        """
        broadcast message to every user
        """
        if getattr(self, "thread", None):
            await self.consumer.channel_layer.group_send(
                self.consumer.thread_name,
                {
                    "type": "chat.message",
                    "message": json.dumps(
                        {
                            "chatId": self.thread.id,
                            "text": self.message,
                            "sent_at": self.msg.sent_at,
                            "sender": {
                                "username": self.msg.sender.username,
                                "email": self.msg.sender.email,
                            },
                        },
                        cls=DjangoJSONEncoder,
                    ),
                    "failed_to_send": self.FAILED_USERS,
                },
            )

    async def save_message(self, user: Union[User, Dict[str, str]]) -> None:
        """
        save each user message to db
        """
        try:
            user = await database_sync_to_async(get_user_model().objects.get)(
                username=user["username"]
            )
            self.consumer.thread = self.thread = await CreateThread()(
                self.consumer, user, "dm", [user, self.sender]
            )
            await self.consumer.channel_layer.group_add(
                self.thread.name, self.consumer.channel_name
            )
            self.msg = await SaveMessage()(self.consumer, self.message)
        except get_user_model().DoesNotExist:
            self.FAILED_USERS.append(user)

    @asynccontextmanager
    async def processMessages(self, user: Dict[str, str]) -> None:
        try:
            yield self.save_message(user)
        finally:
            await self.broadcast_message(user)

    async def __call__(self, users: list) -> None:
        """
        broadcast and save messaged to various users
        """
        for user in users:
            async with self.processMessages(user) as broadcast:
                await broadcast
