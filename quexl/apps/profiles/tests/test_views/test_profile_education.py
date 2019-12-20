import pytest
from django.urls import reverse
from django.utils.timezone import now
from django.utils.timezone import timedelta

from quexl.apps.profiles.models import Education
from quexl.apps.profiles.tests.fixtures import education


def test_edit_profile_education_details(client, generate_access_token1):
    """
    test edit education details for a given profile id
    """
    token, user = generate_access_token1
    username = user.username
    profile_url = reverse("profiles:user_profiles", args=[username])
    response = client.patch(
        profile_url,
        {"education": [education]},
        HTTP_AUTHORIZATION="Bearer %s" % token,
        content_type="application/json",
    )
    assert response.status_code == 200
    assert Education.objects.filter(profile_id=user.profile.id).count() == 1
    assert len(response.data["education"]) == 1
    assert b"Update user profile successfull" in response.content


def test_invalid_education_country(client, generate_access_token1):
    """
    test updating education with invalid country code
    """
    token, user = generate_access_token1
    username = user.username
    profile_url = reverse("profiles:user_profiles", args=[username])
    new_education = education.copy()
    new_education.update({"country": "invalid_country"})
    response = client.patch(
        profile_url,
        {"education": [new_education]},
        HTTP_AUTHORIZATION="Bearer %s" % token,
        content_type="application/json",
    )
    assert response.status_code == 422
    assert b"invalid_country is not a valid country code" in response.content


def test_duplicate_education_info(client, generate_access_token1):
    """
    test duplicate education info
    """
    token, user = generate_access_token1
    username = user.username
    profile_url = reverse("profiles:user_profiles", args=[username])
    response = client.patch(
        profile_url,
        {"education": [education, education]},
        HTTP_AUTHORIZATION="Bearer %s" % token,
        content_type="application/json",
    )
    assert response.status_code == 200
    assert Education.objects.filter(profile_id=user.profile.id).count() == 1
    assert len(response.data["education"]) == 1
    assert b"Update user profile successfull" in response.content


@pytest.mark.parametrize(
    "fieldName",
    [
        ("level"),
        ("school"),
        ("description"),
        ("country"),
        ("course"),
        ("start_date"),
        ("end_date"),
    ],
)
def test_missing_fields_for_education(
    client, fieldName: str, generate_access_token1
) -> None:
    """
    test missing/ required fields for profile education
    """
    token, user = generate_access_token1
    username = user.username
    profile_url = reverse("profiles:user_profiles", args=[username])
    new_education = education.copy()
    new_education.pop(fieldName)
    response = client.patch(
        profile_url,
        {"education": [new_education]},
        HTTP_AUTHORIZATION="Bearer %s" % token,
        content_type="application/json",
    )
    assert response.status_code == 422
    assert response.data["education"][0][fieldName] is not None
    assert b"This field is required." in response.content


@pytest.mark.parametrize(
    "end_date, on_going",
    [
        (now() + timedelta(hours=-2), False),  # past end date
        (now() + timedelta(hours=2), True),  # future end_date
    ],
)
def test_on_going_and_end_date_for_education(
    client, generate_access_token1, end_date, on_going
):
    """
    ensure at least on_going or end_date fields are provided
    """
    token, user = generate_access_token1
    username = user.username
    profile_url = reverse("profiles:user_profiles", args=[username])
    new_education = education.copy()
    new_education["end_date"] = end_date
    response = client.patch(
        profile_url,
        {"education": [new_education]},
        HTTP_AUTHORIZATION="Bearer %s" % token,
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.data["education"][0]["on_going"] == on_going


@pytest.mark.parametrize(
    "choice",
    [("Secondary School"), ("Diploma"), ("Degree"), ("PHD"), ("Masters")],
)
def test_education_level_choices(client, generate_access_token1, choice):
    """
    test all education level choices
    """
    token, user = generate_access_token1
    username = user.username
    profile_url = reverse("profiles:user_profiles", args=[username])
    new_education = education.copy()
    new_education["level"] = choice
    response = client.patch(
        profile_url,
        {"education": [new_education]},
        HTTP_AUTHORIZATION="Bearer %s" % token,
        content_type="application/json",
    )
    assert response.status_code == 200
    assert b"Update user profile successfull" in response.rendered_content


def test_education_level_invalid_choice(client, generate_access_token1):
    """
    test invalid education level value
    """
    token, user = generate_access_token1
    username = user.username
    profile_url = reverse("profiles:user_profiles", args=[username])
    new_education = education.copy()
    new_education.update({"level": "invalid_value"})
    response = client.patch(
        profile_url,
        {"education": [new_education]},
        HTTP_AUTHORIZATION="Bearer %s" % token,
        content_type="application/json",
    )
    assert response.status_code == 422
    assert response.data["education"][0]["level"] is not None
    assert b'\\"invalid_value\\" is not a valid choice.' in response.content
