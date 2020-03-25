"""
test file for parameters
"""
import json

from django.urls import reverse


def test_list_data_files(client, generate_access_token1, create_parameter):
    """test listing of parameters"""
    url = reverse("order:parameters")
    token, _ = generate_access_token1
    response = client.get(url, HTTP_AUTHORIZATION=f"Bearer {token}")
    resp = json.loads(response.content.decode())
    assert response.status_code == 200
    assert resp["status"] == "success"
    assert resp["data"][0]["comment"] == "jpg_to_png"
