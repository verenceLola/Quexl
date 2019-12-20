from rest_framework import serializers

from quexl.apps.profiles.models import Language


class LanguageSerializer(serializers.ModelSerializer):
    """
    serializer user language info
    """

    class Meta:
        fields = ("name", "fluency")
        model = Language

    def create(self, validated_data):
        """
        create language instance and save to db with unique fields handled
        """
        fluency = validated_data.pop("fluency")
        language, _ = Language.objects.get_or_create(**validated_data)
        language.fluency = fluency
        language.save()

        return language
