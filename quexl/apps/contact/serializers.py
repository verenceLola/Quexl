from rest_framework import serializers

from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    """serializers for contact model"""

    class Meta:
        model = Contact
        fields = "__all__"
