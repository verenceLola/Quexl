from typing import Type

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save

from quexl.helpers.fancy_generator import fancy_id_generator


class Thread(models.Model):
    """
    message thread/room model
    """

    class Meta:
        ordering = ("-last_message",)

    participants = models.ManyToManyField(
        get_user_model(),
        through="Participant",
        through_fields=("thread", "user"),
    )
    last_message = models.DateTimeField(db_index=True, blank=True, null=True)
    archived = models.BooleanField(default=False)
    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=20)


class Participant(models.Model):
    """
    django through model
    """

    DELIVERED = "D"
    UNREAD = "UR"
    READ = "R"
    SENT = "S"
    MESSAGE_STATUS = [
        (DELIVERED, "Delivered"),
        (UNREAD, "Unread"),
        (READ, "Read"),
        (SENT, "Sent"),
    ]
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    message_status = models.CharField(
        max_length=20, blank=True, choices=MESSAGE_STATUS, default="D"
    )


class Message(models.Model):
    """
    messages Django model
    """

    class Meta:
        ordering = ("-sent_at",)

    id = models.CharField(
        db_index=True,
        max_length=256,
        default=fancy_id_generator,
        primary_key=True,
        editable=False,
    )
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField(max_length=255)
    sent_at = models.DateTimeField(auto_now_add=True, db_index=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    msg_status = models.CharField(max_length=5, default="S")

    @property
    def status(self) -> str:
        """
        return message status
        """
        states = {"R": "read", "UR": "unread", "D": "delivered", "S": "sent"}

        def setStatus(status: str) -> bool:
            state = all(
                participant.message_status == status
                for participant in Participant.objects.filter(
                    thread=self.thread
                )
            )
            if state:
                self.msg_status = status
                self.save()
            return state

        state = {
            "read": setStatus("R"),
            "unread": setStatus("UR"),
            "delivered": setStatus("D"),
            "sent": setStatus("S"),
        }
        return (
            "read"
            if state["read"]
            else "unread"
            if state["unread"]
            else "delivered"
            if state["delivered"]
            else "sent"
            if state["sent"]
            else states[self.msg_status]
        )


def update_last_message_datetime(
    sender: Type[Message], instance: Message, created: bool, **kwargs
) -> None:
    """
    Update Thread's last_message field when
    a new message is sent.
    """
    if not created:
        return

    Thread.objects.filter(id=instance.thread.id).update(
        last_message=instance.sent_at
    )


post_save.connect(update_last_message_datetime, sender=Message)
