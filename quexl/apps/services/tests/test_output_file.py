import json

from django.urls import reverse


def test_list_output_file(client, generate_access_token1, create_output_file):
    """
    test listing output_file
    """
    URL = reverse("services:output_files")
    token, _ = generate_access_token1
    response = client.get(URL, HTTP_AUTHORIZATION=f"Bearer {token}")
    resp = json.loads(response.content.decode())
    assert response.status_code == 200
    assert resp["status"] == "success"
    assert resp["data"][0]["name"] == "Output file"


def test_get_an_output_file(
    client, generate_access_token1, create_output_file
):
    """
    test geting one output_file
    """
    URL = reverse("services:output_file", args=[create_output_file.id])
    token, _ = generate_access_token1
    response = client.get(URL, HTTP_AUTHORIZATION=f"Bearer {token}")
    resp = json.loads(response.content.decode())
    assert response.status_code == 200
    assert resp["status"] == "success"
    assert resp["data"]["name"] == "Output file"


def test_create_output_file_with_erros(client, generate_access_token1):
    """
    test getting a output file with errors
    """
    token, _ = generate_access_token1
    URL = reverse("services:output_files")
    data = {
        "name": "file",
    }
    data["service"] = "wrongservice"
    data["data_format"] = "badone"
    request = client.post(URL, data, HTTP_AUTHORIZATION=f"Bearer {token}")
    assert request.status_code == 422
    assert (
        request.data["message"]
        == "Create output file failed. Fix the error(s) below"
    )
