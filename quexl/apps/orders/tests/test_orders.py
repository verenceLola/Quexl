"""
test file for orders
"""
import json

from django.urls import reverse


def test_list_orders(client, generate_access_token1, create_data_file):
    """test listing of orders"""
    url = reverse("order:orders")
    token, _ = generate_access_token1
    response = client.get(url, HTTP_AUTHORIZATION=f"Bearer {token}")
    resp = json.loads(response.content.decode())
    assert response.status_code == 200
    assert resp["status"] == "success"
