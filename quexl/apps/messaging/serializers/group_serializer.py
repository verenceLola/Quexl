from django.contrib.auth import get_user_model
from rest_framework import serializers

from quexl.apps.messaging.models import Thread

from .message_serializer import MessageSerializer
from .participant_serializer import ParticipantSerializer


class GroupSerializer(serializers.ModelSerializer):
    """
    serializer threads data
    """

    class Meta:
        model = Thread
        exclude = ("participants", "type", "name")

    members = ParticipantSerializer(many=True, source="participants")
    group_name = serializers.CharField(source="name")

    def create(self, validated_data):
        """
        create a new participant
        """
        members = validated_data.get("participants")
        group_name = validated_data.get("name")
        current_user = self.context["request"].user
        group, _ = Thread.objects.get_or_create(name=group_name, type="group")
        group.participants.add(
            current_user
        )  # add current user as member to group
        for member in members:  # add all members
            participant = get_user_model().objects.get(
                username=member.get("username")
            )
            group.participants.add(participant)
        return group


class GroupMessagesSerializer(GroupSerializer):
    messages = MessageSerializer(many=True, source="message_set")
