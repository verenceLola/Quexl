import pytest
from django.urls import reverse


@pytest.mark.parametrize("fieldName", [("name"), ("fluency")])
def test_required_profile_language_fields(
    client, generate_access_token1, fieldName
):
    """
    test update profile languages info
    """
    token, user = generate_access_token1
    id = user.id
    profile_url = reverse("profiles:user_profiles", args=[id])
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
