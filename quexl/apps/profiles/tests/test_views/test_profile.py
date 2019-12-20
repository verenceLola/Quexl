import pytest
from django.urls import reverse

from quexl.apps.profiles.tests.fixtures import first_name
from quexl.apps.profiles.tests.fixtures import languages
from quexl.apps.profiles.tests.fixtures import last_name
from quexl.apps.profiles.tests.fixtures import profile_description
from quexl.apps.profiles.tests.fixtures import profile_picture
from quexl.apps.profiles.tests.fixtures import profile_title


def test_view_user_profile(client, generate_access_token1):
    """
    test that user profile has all the required fields
    """
    token, user = generate_access_token1
    username = user.username
    profile_url = reverse("profiles:user_profiles", args=[username])
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
    username = user.username
    profile_url = reverse("profiles:user_profiles", args=[username])
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
