"""
test profiles models
"""
from datetime import datetime

import pytest
from django.db import IntegrityError
from freezegun import freeze_time

from quexl.apps.profiles.models import Language
from quexl.apps.profiles.models import Profile
from quexl.apps.profiles.models import Skill


def test_new_profile_has_expected_fields(create_db_user):
    """
    test new profile has all expected fields
    """
    user = create_db_user
    assert Profile.objects.all().count() == 1
    profile = user.profile
    assert profile.user == user
    assert profile.first_name == ""
    assert profile.last_name == ""
    assert profile.profile_picture == ""
    assert profile.personal_description == ""
    assert profile.workexperience_set
    assert profile.address
    assert profile.skills
    assert profile.title == ""
    assert profile.education_set
    assert profile.languages


@freeze_time("2019-10-29 09:00:30")
def test_profile_update_time(django_user_model):
    """
    test updating profile updates the updated_at field
    """
    user = django_user_model.objects.create(
        username="verence", password="Pass123", email="email@quexl.com"
    )
    profile = user.profile
    profile.last_name = "lastname"  # update profile
    assert (
        profile.updated_at.timestamp()
        == datetime(2019, 10, 29, 9, 00, 30).timestamp()
    )


def test_update_profile_with_duplicate_language(create_language):
    """
    test updating profile names with duplicate language fails
    """
    profile = create_language.profile
    dup_language = {"name": "sw"}

    with pytest.raises(IntegrityError):
        Language.objects.create(profile=profile, **dup_language)


def test_update_skill_with_duplicate_address(create_skill):
    """
    test updating profile with dulicate address fails
    """
    profile = create_skill.profile
    dup_skill = {"name": "first"}

    with pytest.raises(IntegrityError):
        Skill.objects.create(profile=profile, **dup_skill)
