from django.core.validators import RegexValidator
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from quexl.apps.profiles.models import Profile

from .address import AddressSerializer
from .education import EducationSerializer
from .language import LanguageSerializer
from .skill import SkillSerializer
from .user import UserSerializer
from .work_experience import WorkExperienceSerializer


class ProfileSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "title",
            "first_name",
            "last_name",
            "profile_description",
            "profile_picture",
            "user",
            "work_experience",
            "education",
            "skills",
            "address",
            "languages",
        ]

    work_experience = WorkExperienceSerializer(
        many=True, source="workexperience_set"
    )
    education = EducationSerializer(many=True, source="education_set")
    skills = SkillSerializer(many=True)
    address = AddressSerializer(many=True)
    user = UserSerializer(read_only=True)
    languages = LanguageSerializer(many=True)
    profile_description = serializers.CharField(
        required=True, source="personal_description"
    )
    first_name = serializers.CharField(
        required=True,
        validators=[
            RegexValidator(
                r"^[a-zA-Z]+$", "name should only have alphabet characters"
            )
        ],
    )
    last_name = serializers.CharField(
        required=True,
        validators=[
            RegexValidator(
                r"^[a-zA-Z]+$", "name should only have alphabet characters"
            )
        ],
    )
    profile_picture = serializers.URLField()
