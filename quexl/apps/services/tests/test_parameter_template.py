import json

from django.urls import reverse


def test_list_parameter_template(
    client, generate_access_token1, create_parameter_template
):
    """
    test listing parameter_template
    """
    URL = reverse("services:parameter_templates")
    token, user = generate_access_token1
    response = client.get(URL, HTTP_AUTHORIZATION=f"Bearer {token}")
    resp = json.loads(response.content.decode())
    assert response.status_code == 200
    assert resp["status"] == "success"
    assert resp["data"][0]["name"] == "Image"


def test_get_an_parameter_template(
    client, generate_access_token1, create_parameter_template
):
    """
    test geting one parameter_template
    """
    URL = reverse(
        "services:parameter_template", args=[create_parameter_template.id]
    )
    token, user = generate_access_token1
    response = client.get(URL, HTTP_AUTHORIZATION=f"Bearer {token}")
    resp = json.loads(response.content.decode())
    assert response.status_code == 200
    assert resp["status"] == "success"
    assert resp["data"]["name"] == "Image"


def test_create_parameter_template_with_errors(client, generate_access_token1):
    """
    test getting a parameter template with errors
    """
    token, user = generate_access_token1
    URL = reverse("services:parameter_templates")
    data = {
        "name": "parameter template",
    }
    data["service"] = "wrongservice"
    data["data_format"] = "badone"
    request = client.post(URL, data, HTTP_AUTHORIZATION=f"Bearer {token}")
    assert request.status_code == 400
    assert (
        request.data["message"]
        == "Create parameter template failed. Fix the error(s) below"
    )
