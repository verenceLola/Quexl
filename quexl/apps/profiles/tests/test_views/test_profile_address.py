import pytest
from django.urls import reverse

from quexl.apps.profiles.models import Address
from quexl.apps.profiles.tests.fixtures import address


def test_edit_profile_address(client, generate_access_token1):
    """
    test editing profile address
    """
    token, user = generate_access_token1
    username = user.username
    profile_url = reverse("profiles:user_profiles", args=[username])
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
    username = user.username
    profile_url = reverse("profiles:user_profiles", args=[username])
    response = client.patch(
        profile_url,
        {"address": [address, address]},
        HTTP_AUTHORIZATION="Bearer " + token,
        content_type="application/json",
    )
    response.render()
    assert Address.objects.filter(profile_id=user.profile.id).count() == 1
    assert len(response.data["address"]) == 1
    assert b"Update user profile successfull" in response.content


def test_invalid_country_in_profile_address(client, generate_access_token1):
    """
    test adding address with invalid country code
    """
    token, user = generate_access_token1
    username = user.username
    profile_url = reverse("profiles:user_profiles", args=[username])
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
    username = user.username
    profile_url = reverse("profiles:user_profiles", args=[username])
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
    username = user.username
    profile_url = reverse("profiles:user_profiles", args=[username])
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
