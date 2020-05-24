import pytest
from django.urls import reverse

from quexl.apps.profiles.models import Skill
from quexl.apps.profiles.tests.fixtures import skill


def test_edit_profile_skill_info(client, generate_access_token1):
    """
    test create profile skills info
    """
    token, user = generate_access_token1
    id = user.id
    profile_url = reverse("profiles:user_profiles", args=[id])
    response = client.patch(
        profile_url,
        {"skills": [skill]},
        HTTP_AUTHORIZATION="Bearer %s" % token,
        content_type="application/json",
    )
    assert response.status_code == 200
    assert Skill.objects.filter(profile_id=user.profile.id).count() == 1
    assert len(response.data["skills"]) == 1
    assert b"Update user profile successfull" in response.rendered_content


def test_duplicate_skills(client, generate_access_token1):
    """
    test duplicate skill info for a given profile
    """
    token, user = generate_access_token1
    id = user.id
    profile_url = reverse("profiles:user_profiles", args=[id])
    response = client.patch(
        profile_url,
        {"skills": [skill, skill]},
        HTTP_AUTHORIZATION="Bearer %s" % token,
        content_type="application/json",
    )
    assert response.status_code == 200
    assert Skill.objects.filter(profile_id=user.profile.id).count() == 1
    assert len(response.data["skills"]) == 1
    assert b"Update user profile successfull" in response.rendered_content


def test_invalid_skill_expertise_value(client, generate_access_token1):
    """
    test invalid skill expertice value
    """
    token, user = generate_access_token1
    id = user.id
    profile_url = reverse("profiles:user_profiles", args=[id])
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
    id = user.id
    profile_url = reverse("profiles:user_profiles", args=[id])
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


@pytest.mark.parametrize("fieldName", [("name"), ("expertise")])
def test_required_skills_fields(client, generate_access_token1, fieldName):
    """
    test required fields for skills info
    """
    token, user = generate_access_token1
    id = user.id
    profile_url = reverse("profiles:user_profiles", args=[id])
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
