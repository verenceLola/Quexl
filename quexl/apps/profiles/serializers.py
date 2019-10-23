from rest_framework import serializers
from django.contrib.auth import get_user_model
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework.exceptions import ValidationError
from django.core.validators import RegexValidator
from quexl.apps.profiles.models import (
    Profile,
    Address,
    WorkExperience,
    Education,
    Skill,
    Language,
)
from django_countries import countries
from phonenumber_field.validators import validate_international_phonenumber
from django.utils import timezone


class FieldSerializerWrapper(serializers.ModelSerializer):
    """
    wrapper for related fields serializers
    """

    def validate_country(self, value):
        """
        validate country code
        """
        if countries.countries.get(value.upper()):
            return value.upper()
        raise ValidationError("%s is not a valid country code" % value)


class AddressSerializer(FieldSerializerWrapper):
    """
    address serializer
    """

    class Meta:
        exclude = ("profile", "id")
        model = Address

    street_address_1 = serializers.CharField(required=True)
    city = serializers.CharField(
        required=True,
        validators=[
            RegexValidator(
                r"^[A-Za-z]+$",
                message="value should be string characters only",
            )
        ],
    )
    city_area = serializers.CharField(
        required=True,
        validators=[
            RegexValidator(
                r"^[A-Za-z]+$",
                message="value should be string characters only",
            )
        ],
    )
    postal_code = serializers.IntegerField(required=True)
    country = serializers.CharField(required=True)
    country_area = serializers.CharField(
        required=True,
        validators=[
            RegexValidator(
                r"^[A-Za-z]+$",
                message="value should be string characters only",
            )
        ],
    )
    phone = serializers.CharField(
        required=True, validators=[validate_international_phonenumber]
    )

    def create(self, validated_data):
        """
        create user address info
        """
        address, _ = Address.objects.get_or_create(
            **validated_data
        )  # prevent creating similar address info
        return address


class WorkExperienceSerializer(FieldSerializerWrapper):
    """
    work experience serializer
    """

    class Meta:
        exclude = ("profile", "id")
        model = WorkExperience

    description = serializers.CharField(required=True)
    on_going = serializers.BooleanField(read_only=True)
    employee = serializers.CharField(required=True)
    start_date = serializers.DateTimeField(required=True)
    end_date = serializers.DateTimeField(required=True)
    country = serializers.CharField(required=True)
    role = serializers.CharField(required=True)

    def create(self, validated_data):
        """
        create user work experience
        """
        employee = validated_data.pop("employee")
        role = validated_data.pop("role")
        profile = validated_data.pop("profile")
        work, _ = WorkExperience.objects.get_or_create(
            employee=employee, role=role, profile=profile
        )
        work.start_date = validated_data["start_date"]
        work.end_date = validated_data["end_date"]
        work.description = validated_data["description"]
        work.country = validated_data["country"]
        work.save()
        return work

    def validate_start_date(self, value):
        """
        validate work start date
        """
        if value > timezone.now():  # start_date is future date
            raise ValidationError("Start date cannot be a future date")
        return value

    def validate(self, data: dict):
        """
        validate work experience data
        """
        start_date = data.get("start_date", None)
        end_date = data.get("end_date", None)
        if not start_date or not end_date:
            return super(WorkExperienceSerializer, self).validate(data)
        if start_date > end_date:  # start_date cannot be later than end_date
            raise ValidationError(
                {"end_date": "End date cannot be earlier than the start date"}
            )
        return data


class EducationSerializer(FieldSerializerWrapper):
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

    def create(self, validated_data: dict):
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


class SkillSerializer(serializers.ModelSerializer):
    """
    skill serializer
    """

    class Meta:
        exclude = ("id", "profile")
        model = Skill

    def create(self, validated_data):
        """
        create new skill
        """
        expertise = validated_data.pop("expertise")
        skill, _ = Skill.objects.get_or_create(**validated_data)
        skill.expertise = expertise
        skill.save()
        return skill


class UserSerializer(serializers.ModelSerializer):
    """
    serializer for user info
    """

    class Meta:
        fields = ("email", "username")
        model = get_user_model()


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
