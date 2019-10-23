from django.db import models
from quexl.apps.account.models import User
from django.core.validators import RegexValidator
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from quexl.helpers.fancy_generator import fancy_id_generator
from languages.fields import LanguageField
from django.utils.timezone import now


class Profile(models.Model):
    """
    user profile
    """

    id = models.CharField(
        primary_key=True,
        default=fancy_id_generator,
        editable=False,
        db_index=True,
        max_length=256,
    )
    title = models.CharField(
        max_length=10,
        choices=[("Mister", "Mr"), ("Miss", "Miss"), ("Missis", "Mrs")],
    )
    first_name = models.CharField(
        max_length=16,
        validators=[
            RegexValidator(
                r"^[a-zA-Z]+$",
                "first name should only have alphabet characters",
            )
        ],
        blank=True,
    )
    last_name = models.CharField(
        max_length=16,
        validators=[
            RegexValidator(
                r"^[a-zA-Z]+$",
                "last name should only have alphabet characters",
            )
        ],
        blank=True,
    )
    profile_picture = models.URLField(blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    personal_description = models.TextField(max_length=300, blank=True)
    updated_at = models.DateTimeField(auto_now=True)


class Address(models.Model):
    id = models.CharField(
        db_index=True,
        max_length=256,
        default=fancy_id_generator,
        primary_key=True,
        editable=False,
    )
    street_address_1 = models.CharField(max_length=256, blank=True)
    city = models.CharField(max_length=256, blank=True)
    city_area = models.CharField(max_length=128, blank=True)
    postal_code = models.IntegerField(blank=True)
    country = CountryField()
    country_area = models.CharField(max_length=128, blank=True)
    phone = PhoneNumberField(blank=True)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="address"
    )

    class Meta:
        ordering = ("pk",)

    @property
    def address(self):
        return "%s" % self.city

    def __repr__(self):
        return (
            "Address(street_address_1=%r, "
            "city=%r, postal_code=%r, country=%r, "
            "country_area=%r, phone=%r)"
            % (
                self.street_address_1,
                self.city,
                self.postal_code,
                self.country,
                self.country_area,
                self.phone,
            )
        )


class WorkEducationAbstract(models.Model):
    """
    abstract class for holding common info between user progile info
    """

    id = models.CharField(
        primary_key=True,
        default=fancy_id_generator,
        editable=False,
        db_index=True,
        max_length=256,
    )
    country = CountryField(blank=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    description = models.TextField(max_length=300, blank=True)
    # on_going = models.BooleanField(default=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    @property
    def on_going(self):
        """
        determine if activity is on_going or not
        """
        return now() < self.end_date


class Education(WorkEducationAbstract):
    """
    user education info
    """

    LEVEL_CHOICE = [
        ("Secondary School", "Sec"),
        ("Diploma", "Dip"),
        ("Degree", "Deg"),
        ("PHD", "Phd"),
        ("Masters", "Mas"),
    ]
    course = models.CharField(max_length=100, blank=True)
    school = models.CharField(max_length=100, blank=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICE, blank=True)

    class Meta:
        """
        user can't have same education level in same school for the same course
        """

        unique_together = ("school", "level", "profile", "course")


class WorkExperience(WorkEducationAbstract):
    """
    user work experience info
    """

    role = models.CharField(max_length=50, blank=True)
    employee = models.CharField(max_length=100, blank=True)

    class Meta:
        """
        user cannot have same role in same company at the same time
        """

        unique_together = ("role", "employee", "profile", "start_date")


class Skill(models.Model):
    """
    user skills info
    """

    id = models.CharField(
        primary_key=True,
        default=fancy_id_generator,
        editable=False,
        db_index=True,
        max_length=256,
    )
    name = models.CharField(max_length=20)
    expertise = models.CharField(
        max_length=15,
        choices=[("beginner", "B"), ("intermediate", "I"), ("expert", "E")],
    )
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="skills"
    )

    class Meta:
        unique_together = ("profile", "name")


class Language(models.Model):
    """
    user languages
    """

    id = models.CharField(
        primary_key=True,
        default=fancy_id_generator,
        editable=False,
        db_index=True,
        max_length=256,
    )
    FLUENCY = [
        ("Elementary", 0),
        ("limited", 1),
        ("Professional", 2),
        ("Full Professional", 3),
        ("Native", 4),
    ]
    name = LanguageField()
    fluency = models.CharField(max_length=15, choices=FLUENCY)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="languages"
    )

    class Meta:
        unique_together = ("profile", "name")
