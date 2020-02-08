import json

from django.urls import reverse


def test_list_data_formats(client, generate_access_token1, create_data_format):
    """
    test listing data_formats
    """
    URL = reverse("services:data_formats")
    token, user = generate_access_token1
    response = client.get(URL, HTTP_AUTHORIZATION=f"Bearer {token}")
    resp = json.loads(response.content.decode())
    assert response.status_code == 200
    assert resp["status"] == "success"
    assert resp["data"][0]["name"] == "data format"


def test_get_a_category(client, generate_access_token1, create_data_format):
    """
    test geting one data format
    """
    URL = reverse("services:data_format", args=[create_data_format.id])
    token, user = generate_access_token1
    response = client.get(URL, HTTP_AUTHORIZATION=f"Bearer {token}")
    resp = json.loads(response.content.decode())
    assert response.status_code == 200
    assert resp["status"] == "success"
    assert resp["data"]["name"] == create_data_format.name
