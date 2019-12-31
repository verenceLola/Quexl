"""
utility functions for websocket connections
"""
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.db.models import Q

from quexl.apps.account.models import User
from quexl.apps.messaging.models import Message
from quexl.apps.messaging.models import Thread

from .md5 import md5


@database_sync_to_async
def get_or_create_thread(
    self: AsyncJsonWebsocketConsumer,
    to: User,
    type: str,
    participants: list = [],
) -> Thread:  # TODO: modify function to make it idempotent for asynchronicy
    """
    get or create chat thread/ group
    """
    sender = self.scope["user"]
    thread_name1 = md5(to.username.lower() + sender.username.lower())
    thread_name2 = md5(sender.username.lower() + to.username.lower())
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


@database_sync_to_async
def save_message_to_db(self: AsyncJsonWebsocketConsumer, text: str) -> Message:
    """"
    save message to db
    """
    sender = self.scope["user"]
    msg = Message.objects.create(sender=sender, text=text, thread=self.thread)
    return msg
