from typing import Dict
from typing import Union

from rest_framework import serializers

from quexl.apps.profiles.models import Profile
from quexl.apps.profiles.models import Skill


class SkillSerializer(serializers.ModelSerializer):
    """
    skill serializer
    """

    class Meta:
        exclude = ("id", "profile")
        model = Skill

    def create(self, validated_data: Dict[str, Union[str, Profile]]) -> Skill:
        """
        create new skill
        """
        expertise = validated_data.pop("expertise")
        skill, _ = Skill.objects.get_or_create(**validated_data)
        skill.expertise = expertise
        skill.save()

        return skill
