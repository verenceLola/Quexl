from rest_framework import serializers

from quexl.apps.messaging.models import Thread

from .message_serializer import MessageSerializer


class DMMessagesSerializer(serializers.ModelSerializer):
    """
    serialize threads data
    """

    class Meta:
        model = Thread
        exclude = ("name", "participants", "type")

    messages = MessageSerializer(many=True, source="message_set")
