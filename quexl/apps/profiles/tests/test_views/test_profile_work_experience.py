import pytest
from django.urls import reverse
from django.utils.timezone import now
from django.utils.timezone import timedelta

from quexl.apps.profiles.models import WorkExperience
from quexl.apps.profiles.tests.fixtures import work_experience


def test_create_work_experience(client, generate_access_token1):
    """
    test creating work experience for user profile
    """
    token, user = generate_access_token1
    username = user.username
    profile_url = reverse("profiles:user_profiles", args=[username])
    response = client.patch(
        profile_url,
        {"work_experience": [work_experience]},
        HTTP_AUTHORIZATION="Bearer %s" % token,
        content_type="application/json",
    )
    assert response.status_code == 200
    assert b"Update user profile successfull" in response.content
    assert (
        WorkExperience.objects.filter(profile_id=user.profile.id).count() == 1
    )


def test_add_duplicate_profile_work_experience(client, generate_access_token1):
    """
    test user cannot add duplicate work experience info
    """
    token, user = generate_access_token1
    username = user.username
    profile_url = reverse("profiles:user_profiles", args=[username])
    response = client.patch(
        profile_url,
        {"work_experience": [work_experience, work_experience]},
        HTTP_AUTHORIZATION="Bearer %s" % token,
        content_type="application/json",
    )
    assert response.status_code == 200
    assert (
        WorkExperience.objects.filter(profile_id=user.profile.id).count() == 1
    )
    assert b"Update user profile successfull" in response.content
    assert len(response.data["work_experience"]) == 1


def test_work_experience_start_data(client, generate_access_token1):
    """
    test setting work experience to future date
    """
    token, user = generate_access_token1
    username = user.username
    profile_url = reverse("profiles:user_profiles", args=[username])
    new_work_experience = work_experience.copy()
    new_work_experience.update({"start_date": now() + timedelta(hours=3)})
    response = client.patch(
        profile_url,
        {"work_experience": [new_work_experience]},
        HTTP_AUTHORIZATION="Bearer %s" % token,
        content_type="application/json",
    )
    assert response.status_code == 422
    assert b"Start date cannot be a future date" in response.content


def test_work_experience_end_date(client, generate_access_token1):
    """
    test end date for work experience is valid
    """
    token, user = generate_access_token1
    username = user.username
    profile_url = reverse("profiles:user_profiles", args=[username])
    new_work_experience = work_experience.copy()
    new_work_experience.update({"end_date": "2018-10-25 22:58:55.216869+03"})
    response = client.patch(
        profile_url,
        {"work_experience": [new_work_experience]},
        HTTP_AUTHORIZATION="Bearer %s" % token,
        content_type="application/json",
    )
    assert response.status_code == 422
    assert (
        b"End date cannot be earlier than the start date" in response.content
    )


@pytest.mark.parametrize(
    "fieldName",
    [
        ("description"),
        ("employee"),
        ("start_date"),
        ("end_date"),
        ("country"),
        ("role"),
    ],
)
def test_required_work_experience_fields(
    client, generate_access_token1, fieldName
):
    """
    test required work experience fields
    """
    token, user = generate_access_token1
    username = user.username
    profile_url = reverse("profiles:user_profiles", args=[username])
    new_work_experience = work_experience.copy()
    new_work_experience.pop(fieldName)
    response = client.patch(
        profile_url,
        {"work_experience": [new_work_experience]},
        HTTP_AUTHORIZATION="Bearer %s" % token,
        content_type="application/json",
    )
    assert response.status_code == 422
    assert response.data["work_experience"][0][fieldName] is not None
    assert b"This field is required." in response.content
