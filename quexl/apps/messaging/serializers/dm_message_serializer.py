from rest_framework import serializers

from quexl.apps.messaging.models import Thread

from .message_serializer import MessageSerializer
from .participant_serializer import ParticipantSerializer


class DMMessagesSerializer(serializers.ModelSerializer):
    """
    serialize threads data
    """

    class Meta:
        model = Thread
        exclude = ("name", "type")

    participants = ParticipantSerializer(many=True)
    messages = MessageSerializer(many=True, source="message_set")
