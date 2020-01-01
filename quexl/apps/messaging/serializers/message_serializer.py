from rest_framework import serializers

from quexl.apps.messaging.models import Message

from .participant_serializer import ParticipantSerializer


class MessageSerializer(serializers.ModelSerializer):
    """
    serializer user message
    """

    class Meta:
        model = Message
        exclude = ("msg_status", "thread")

    sender = ParticipantSerializer()
    status = serializers.CharField()
