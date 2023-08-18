"""
utility functions for websocket connections
"""
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.db.models import Q

from quexl.apps.account.models import User
from quexl.apps.messaging.models import Thread

from ..md5 import MD5


class CreateThread:
    """
    get or create thread object
    """

    @staticmethod
    @database_sync_to_async
    def __call__(
        self: AsyncJsonWebsocketConsumer,
        to: User,
        type: str,
        participants: list = [],
    ) -> (
        Thread
    ):  # TODO: modify function to make it idempotent for asynchronicy
        """
        get or create chat thread/ group
        """
        sender = self.scope["user"]
        thread_name1 = MD5()(to.username.lower() + sender.username.lower())
        thread_name2 = MD5()(sender.username.lower() + to.username.lower())
        thread_filter = Thread.objects.filter(
            (Q(name=thread_name1) | Q(name=thread_name2)) & Q(type="dm")
        )
        thread = (
            Thread.objects.create(name=thread_name1, type=type)
            if thread_filter.count() == 0
            else thread_filter.first()
        )
        self.thread_name = thread.name
        for participant in participants:
            thread.participants.add(participant)
        return thread
