"""
test file for orders
"""
import json

from django.urls import reverse


def test_list_data_files(client, generate_access_token1, create_data_file):
    """test listing of orders"""
    url = reverse("order:orders")
    token, user = generate_access_token1
    response = client.get(url, HTTP_AUTHORIZATION=f"Bearer {token}")
    resp = json.loads(response.content.decode())
    assert response.status_code == 200
    assert resp["status"] == "success"


# @pytest.mark.django_db(transaction=True)
# def test_refresh_order(client, generate_access_token1, create_order):
#     """test listing of orders"""
#     url = reverse("order:refresh order", args=[create_order.id])
#     token, user = generate_access_token1
#     response = client.get(url, HTTP_AUTHORIZATION=F'Bearer {token}')
#     resp = json.loads(response.content.decode())
#     assert response.status_code == 200
#     assert resp["status"] == "success"
