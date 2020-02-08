import json

from django.urls import reverse


def test_list_parameter_option(
    client, generate_access_token1, create_parameter_option
):
    """
    test listing parameter_option
    """
    URL = reverse("services:parameter_options")
    token, user = generate_access_token1
    response = client.get(URL, HTTP_AUTHORIZATION=f"Bearer {token}")
    resp = json.loads(response.content.decode())
    assert response.status_code == 200
    assert resp["status"] == "success"
    assert resp["data"][0]["short_name"] == "Parameter option"


def test_get_an_parameter_option(
    client, generate_access_token1, create_parameter_option
):
    """
    test geting one parameter_option
    """
    URL = reverse(
        "services:parameter_option", args=[create_parameter_option.id]
    )
    token, user = generate_access_token1
    response = client.get(URL, HTTP_AUTHORIZATION=f"Bearer {token}")
    resp = json.loads(response.content.decode())
    assert response.status_code == 200
    assert resp["status"] == "success"
    assert resp["data"]["short_name"] == "Parameter option"


def test_create_parameter_option_with_erros(client, generate_access_token1):
    """
    test getting a parameter option with errors
    """
    token, user = generate_access_token1
    URL = reverse("services:parameter_options")
    data = {
        "short_name": "parameter option",
    }
    data["parameter"] = "wrongservice"
    request = client.post(URL, data, HTTP_AUTHORIZATION=f"Bearer {token}")
    assert request.status_code == 422
    assert (
        request.data["message"]
        == "Create parameter option failed. Fix the error(s) below"
    )
