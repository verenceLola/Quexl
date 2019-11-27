from rest_framework import serializers
from quexl.apps.messaging.models import Thread, Message
from django.contrib.auth import get_user_model


class ParticipantSerializer(serializers.Serializer):

    username = serializers.CharField()
    email = serializers.CharField(read_only=True)

    def validate_username(self, value):
        """
        ensure the specified username exists
        """
        try:
            get_user_model().objects.get(username=value)
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError(
                f"User with username {value} doesn't exist"
            )
        return value


class MessageSerializer(serializers.ModelSerializer):
    """
    serializer user message
    """

    class Meta:
        model = Message
        exclude = ("msg_status", "thread")

    sender = ParticipantSerializer()
    status = serializers.CharField()


class DMMessagesSerializer(serializers.ModelSerializer):
    """
    serialize threads data
    """

    class Meta:
        model = Thread
        exclude = ("name", "type")

    participants = ParticipantSerializer(many=True)
    messages = MessageSerializer(many=True, source="message_set")


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
