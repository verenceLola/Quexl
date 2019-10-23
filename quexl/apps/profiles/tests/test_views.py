"""
test profiles view
"""
from django.urls import reverse
import pytest
from quexl.apps.profiles.tests.fixtures import (
    profile_title,
    address,
    first_name,
    languages,
    last_name,
    profile_description,
    profile_picture,
    work_experience,
    education,
    skill,
)
from quexl.apps.profiles.models import (
    Address,
    WorkExperience,
    Education,
    Skill,
)
from django.utils.timezone import now, timedelta


def test_view_user_profile(client, generate_access_token1):
    """
    test that user profile has all the required fields
    """
    token, user = generate_access_token1
    profile_id = user.profile.id
    profile_url = reverse("profiles:user_profiles", args=[profile_id])
    response = client.get(profile_url, HTTP_AUTHORIZATION="Bearer " + token)
    assert response.status_code == 200
    assert response.data["title"] == ""
    assert response.data["first_name"] == ""
    assert response.data["last_name"] == ""
    assert response.data["profile_description"] == ""
    assert response.data["profile_picture"] == ""
    assert response.data["work_experience"] == []
    assert response.data["skills"] == []
    assert response.data["education"] == []
    assert response.data["address"] == []
    assert response.data["languages"] == []
    assert response.data["user"]["email"] == user.email
    assert response.data["user"]["username"] == user.username


@pytest.mark.parametrize(
    "field_value, expected_value",
    [
        (profile_title, profile_title),
        (first_name, first_name),
        (languages, languages),
        (last_name, last_name),
        (profile_description, profile_description),
        (profile_picture, profile_picture),
    ],
)
def test_edit_profile_fields_correctly(
    client, generate_access_token1, field_value, expected_value
):
    """
    test editing profile fields
    """
    token, user = generate_access_token1
    profile_id = user.profile.id
    profile_url = reverse("profiles:user_profiles", args=[profile_id])
    response = client.patch(
        profile_url,
        field_value,
        HTTP_AUTHORIZATION="Bearer " + token,
        content_type="application/json",
    )
    assert response.status_code == 200
    response.render()
    assert (
        response.data[[*field_value][0]] == expected_value[[*field_value][0]]
    )


def test_edit_profile_address(client, generate_access_token1):
    """
    test editing profile address
    """
    token, user = generate_access_token1
    profile_id = user.profile.id
    profile_url = reverse("profiles:user_profiles", args=[profile_id])
    response = client.patch(
        profile_url,
        {"address": [address]},
        HTTP_AUTHORIZATION="Bearer " + token,
        content_type="application/json",
    )
    response.render()
    assert response.status_code == 200


def test_add_duplicate_profile_address(client, generate_access_token1):
    """
    test adding duplicate profile addresses
    """
    token, user = generate_access_token1
    profile_id = user.profile.id
    profile_url = reverse("profiles:user_profiles", args=[profile_id])
    response = client.patch(
        profile_url,
        {"address": [address, address]},
        HTTP_AUTHORIZATION="Bearer " + token,
        content_type="application/json",
    )
    response.render()
    assert Address.objects.filter(profile_id=profile_id).count() == 1
    assert len(response.data["address"]) == 1
    assert b"Update user profile successfull" in response.content


def test_invalid_country_in_profile_address(client, generate_access_token1):
    """
    test adding address with invalid country code
    """
    token, user = generate_access_token1
    profile_id = user.profile.id
    profile_url = reverse("profiles:user_profiles", args=[profile_id])
    # update country value
    new_address = address.copy()
    new_address.update({"country": "invalid_country_code"})
    response = client.patch(
        profile_url,
        {"address": [new_address]},
        HTTP_AUTHORIZATION="Bearer  %s" % token,
        content_type="application/json",
    )
    response.render()
    assert response.status_code == 422
    assert b"Update user profile failed." in response.content
    assert (
        b"%s is not a valid country code" % "invalid_country_code".encode()
        in response.content
    )


@pytest.mark.parametrize(
    "fieldName", [("city"), ("city_area"), ("country_area")]
)
def test_invalid_address_fields(client, generate_access_token1, fieldName):
    token, user = generate_access_token1
    profile_id = user.profile.id
    profile_url = reverse("profiles:user_profiles", args=[profile_id])
    # update fieldName value to invalid string
    new_address = address.copy()
    new_address[fieldName] = "7868strin"
    response = client.patch(
        profile_url,
        {"address": [new_address]},
        HTTP_AUTHORIZATION="Bearer %s" % token,
        content_type="application/json",
    )
    response.render()
    assert response.status_code == 422
    assert b"Update user profile failed." in response.content
    assert b"value should be string characters only" in response.content


@pytest.mark.parametrize(
    "fieldName",
    [
        ("city"),
        ("city_area"),
        ("country_area"),
        ("street_address_1"),
        ("postal_code"),
        ("country"),
        ("phone"),
    ],
)
def test_required_field_for_profile_address(
    client, generate_access_token1, fieldName
):
    """
    test all required fields for profile address
    """
    token, user = generate_access_token1
    profile_id = user.profile.id
    profile_url = reverse("profiles:user_profiles", args=[profile_id])
    new_address = address.copy()
    new_address.pop(fieldName)
    response = client.patch(
        profile_url,
        {"address": [new_address]},
        HTTP_AUTHORIZATION="Bearer %s" % token,
        content_type="application/json",
    )
    assert response.status_code == 422
    assert response.data["address"][0][fieldName] is not None
    assert b"This field is required." in response.content


def test_create_work_experience(client, generate_access_token1):
    """
    test creating work experience for user profile
    """
    token, user = generate_access_token1
    profile_id = user.profile.id
    profile_url = reverse("profiles:user_profiles", args=[profile_id])
    response = client.patch(
        profile_url,
        {"work_experience": [work_experience]},
        HTTP_AUTHORIZATION="Bearer %s" % token,
        content_type="application/json",
    )
    assert response.status_code == 200
    assert b"Update user profile successfull" in response.content
    assert WorkExperience.objects.filter(profile_id=profile_id).count() == 1


def test_add_duplicate_profile_work_experience(client, generate_access_token1):
    """
    test user cannot add duplicate work experience info
    """
    token, user = generate_access_token1
    profile_id = user.profile.id
    profile_url = reverse("profiles:user_profiles", args=[profile_id])
    response = client.patch(
        profile_url,
        {"work_experience": [work_experience, work_experience]},
        HTTP_AUTHORIZATION="Bearer %s" % token,
        content_type="application/json",
    )
    assert response.status_code == 200
    assert WorkExperience.objects.filter(profile_id=profile_id).count() == 1
    assert b"Update user profile successfull" in response.content
    assert len(response.data["work_experience"]) == 1


def test_work_experience_start_data(client, generate_access_token1):
    """
    test setting work experience to future date
    """
    token, user = generate_access_token1
    profile_id = user.profile.id
    profile_url = reverse("profiles:user_profiles", args=[profile_id])
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
    profile_id = user.profile.id
    profile_url = reverse("profiles:user_profiles", args=[profile_id])
    new_work_experience = work_experience.copy()
    new_work_experience.update({"end_date": "2018-10-25 22:58:55.216869+03"})
    response = client.patch(
        profile_url,
        {"work_experience": [new_work_experience]},
        HTTP_AUTHORIZATION="Bearer %s" % token,
        content_type="application/json",
    )
    assert response.status_code == 422
    # assert response.data['work_experience']
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
    profile_id = user.profile.id
    profile_url = reverse("profiles:user_profiles", args=[profile_id])
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


def test_edit_profile_education_details(client, generate_access_token1):
    """
    test edit education details for a given profile id
    """
    token, user = generate_access_token1
    profile_id = user.profile.id
    profile_url = reverse("profiles:user_profiles", args=[profile_id])
    response = client.patch(
        profile_url,
        {"education": [education]},
        HTTP_AUTHORIZATION="Bearer %s" % token,
        content_type="application/json",
    )
    assert response.status_code == 200
    assert Education.objects.filter(profile_id=profile_id).count() == 1
    assert len(response.data["education"]) == 1
    assert b"Update user profile successfull" in response.content


def test_invalid_education_country(client, generate_access_token1):
    """
    test updating education with invalid country code
    """
    token, user = generate_access_token1
    profile_id = user.profile.id
    profile_url = reverse("profiles:user_profiles", args=[profile_id])
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
    profile_id = user.profile.id
    profile_url = reverse("profiles:user_profiles", args=[profile_id])
    response = client.patch(
        profile_url,
        {"education": [education, education]},
        HTTP_AUTHORIZATION="Bearer %s" % token,
        content_type="application/json",
    )
    assert response.status_code == 200
    assert Education.objects.filter(profile_id=profile_id).count() == 1
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
    profile_id = user.profile.id
    profile_url = reverse("profiles:user_profiles", args=[profile_id])
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
    profile_id = user.profile.id
    profile_url = reverse("profiles:user_profiles", args=[profile_id])
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


def test_edit_profile_skill_info(client, generate_access_token1):
    """
    test create profile skills info
    """
    token, user = generate_access_token1
    profile_id = user.profile.id
    profile_url = reverse("profiles:user_profiles", args=[profile_id])
    response = client.patch(
        profile_url,
        {"skills": [skill]},
        HTTP_AUTHORIZATION="Bearer %s" % token,
        content_type="application/json",
    )
    assert response.status_code == 200
    assert Skill.objects.filter(profile_id=profile_id).count() == 1
    assert len(response.data["skills"]) == 1
    assert b"Update user profile successfull" in response.rendered_content


def test_duplicate_skills(client, generate_access_token1):
    """
    test duplicate skill info for a given profile
    """
    token, user = generate_access_token1
    profile_id = user.profile.id
    profile_url = reverse("profiles:user_profiles", args=[profile_id])
    response = client.patch(
        profile_url,
        {"skills": [skill, skill]},
        HTTP_AUTHORIZATION="Bearer %s" % token,
        content_type="application/json",
    )
    assert response.status_code == 200
    assert Skill.objects.filter(profile_id=profile_id).count() == 1
    assert len(response.data["skills"]) == 1
    assert b"Update user profile successfull" in response.rendered_content


def test_invalid_skill_expertise_value(client, generate_access_token1):
    """
    test invalid skill expertice value
    """
    token, user = generate_access_token1
    profile_id = user.profile.id
    profile_url = reverse("profiles:user_profiles", args=[profile_id])
    new_skill = skill.copy()
    new_skill.update({"expertise": "invalid_value"})
    response = client.patch(
        profile_url,
        {"skills": [new_skill]},
        HTTP_AUTHORIZATION="Bearer %s" % token,
        content_type="application/json",
    )
    assert response.status_code == 422
    assert response.data["skills"][0]["expertise"] is not None
    assert b'\\"invalid_value\\" is not a valid choice.' in response.content


@pytest.mark.parametrize(
    "choice", [("beginner"), ("intermediate"), ("expert")]
)
def test_skill_expertice_choices(client, generate_access_token1, choice):
    """
    test all skill expertice choices
    """
    token, user = generate_access_token1
    profile_id = user.profile.id
    profile_url = reverse("profiles:user_profiles", args=[profile_id])
    new_skill = skill.copy()
    new_skill["expertise"] = choice
    response = client.patch(
        profile_url,
        {"skills": [new_skill]},
        HTTP_AUTHORIZATION="Bearer %s" % token,
        content_type="application/json",
    )
    assert response.status_code == 200
    assert b"Update user profile successfull" in response.rendered_content


@pytest.mark.parametrize(
    "choice",
    [("Secondary School"), ("Diploma"), ("Degree"), ("PHD"), ("Masters")],
)
def test_education_level_choices(client, generate_access_token1, choice):
    """
    test all education level choices
    """
    token, user = generate_access_token1
    profile_id = user.profile.id
    profile_url = reverse("profiles:user_profiles", args=[profile_id])
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


@pytest.mark.parametrize("fieldName", [("name"), ("expertise")])
def test_required_skills_fields(client, generate_access_token1, fieldName):
    """
    test required fields for skills info
    """
    token, user = generate_access_token1
    profile_id = user.profile.id
    profile_url = reverse("profiles:user_profiles", args=[profile_id])
    new_skill = skill.copy()
    new_skill.pop(fieldName)
    response = client.patch(
        profile_url,
        {"skills": [new_skill]},
        HTTP_AUTHORIZATION="Bearer %s" % token,
        content_type="application/json",
    )
    assert response.status_code == 422
    assert response.data["skills"][0][fieldName] is not None
    assert b"This field is required." in response.content


def test_education_level_invalid_choice(client, generate_access_token1):
    """
    test invalid education level value
    """
    token, user = generate_access_token1
    profile_id = user.profile.id
    profile_url = reverse("profiles:user_profiles", args=[profile_id])
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


@pytest.mark.parametrize("fieldName", [("name"), ("fluency")])
def test_required_profile_language_fields(
    client, generate_access_token1, fieldName
):
    """
    test update profile languages info
    """
    token, user = generate_access_token1
    profile_id = user.profile.id
    profile_url = reverse("profiles:user_profiles", args=[profile_id])
    language = {"name": "sw", "fluency": "limited"}
    language.pop(fieldName)
    response = client.patch(
        profile_url,
        {"languages": [language]},
        HTTP_AUTHORIZATION="Bearer %s" % token,
        content_type="application/json",
    )
    assert response.status_code == 422
    assert response.data["languages"][0][fieldName] is not None
    assert b"This field is required." in response.content
