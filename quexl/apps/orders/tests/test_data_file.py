"""
test file for data files
"""
import json

from django.urls import reverse


def test_list_data_files(client, generate_access_token1, create_data_file):
    """test listing of data files"""
    url = reverse("order:data_files")
    token, user = generate_access_token1
    response = client.get(url, HTTP_AUTHORIZATION=f"Bearer {token}")
    resp = json.loads(response.content.decode())
    assert response.status_code == 200
    assert resp["status"] == "success"
    assert resp["data"][0]["name"] == "Image file"
