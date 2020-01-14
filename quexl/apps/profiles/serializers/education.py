from rest_framework import serializers

from quexl.apps.profiles.models import Education

from .country_serializer_wrapper import CountrySerializerWrapper


class EducationSerializer(CountrySerializerWrapper):
    """
    education serializer
    """

    class Meta:
        exclude = ("profile", "id")
        model = Education

    LEVEL_CHOICE = [
        ("Secondary School", "Sec"),
        ("Diploma", "Dip"),
        ("Degree", "Deg"),
        ("PHD", "Phd"),
        ("Masters", "Mas"),
    ]
    level = serializers.ChoiceField(choices=LEVEL_CHOICE)
    school = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    on_going = serializers.BooleanField(required=False)
    country = serializers.CharField(required=True)
    course = serializers.CharField(required=True)
    start_date = serializers.DateTimeField(required=True)
    end_date = serializers.DateTimeField()

    def create(self, validated_data: dict) -> Education:
        """
        create user education
        """
        level = validated_data.pop("level")
        school = validated_data.pop("school")
        profile = validated_data.pop("profile")
        course = validated_data.pop("course")
        education, _ = Education.objects.get_or_create(
            level=level, course=course, school=school, profile=profile
        )
        education.start_date = validated_data["start_date"]
        education.end_date = validated_data["end_date"]
        education.description = validated_data["description"]
        education.country = validated_data["country"]
        education.save()

        return education
