import json

from django.urls import reverse


def test_list_categories(client, generate_access_token1, create_service):
    """
    test listing services
    """
    URL = reverse("services:services")
    token, user = generate_access_token1
    response = client.get(URL, HTTP_AUTHORIZATION=f"Bearer {token}")
    resp = json.loads(response.content.decode())
    assert response.status_code == 200
    assert resp["status"] == "success"
    assert resp["data"][0]["name"] == "Online file conversion"


def test_get_a_service(client, generate_access_token1, create_service):
    """
    test getting a service
    """
    URL = reverse("services:service", args=[create_service.id])
    token, user = generate_access_token1
    response = client.get(URL, HTTP_AUTHORIZATION=f"Bearer {token}")
    resp = json.loads(response.content.decode())
    assert response.status_code == 200
    assert resp["status"] == "success"
    assert resp["data"]["name"] == "Online file conversion"


def test_get_a_services_with_errors(
    client, generate_access_token1, create_db_user, create_category
):
    """
    test getting a service with price errors
    """
    token, user = generate_access_token1
    URL = reverse("services:services")
    data = {
        "name": "Service 1",
        "delivery_time": "2010-11-01 21:40:53.028781+03",
    }
    data["seller_id"] = "invalid"
    data["category_id"] = "invalid"
    request = client.post(URL, data, HTTP_AUTHORIZATION=f"Bearer {token}")
    assert request.status_code == 422
    assert (
        request.data["message"]
        == "Create service failed. Fix the error(s) below"
    )


def test_create_service_with_bad_category(
    client, generate_access_token1, create_db_user, create_category
):
    """
    test getting a service with price errors
    """
    token, user = generate_access_token1
    URL = reverse("services:services")
    data = {
        "name": "Service 1",
        "delivery_time": "2030-11-01 21:40:53.028781+03",
    }
    data["category_id"] = "invalid"
    data["price"] = {}
    data["price"]["amount"] = "100"
    request = client.post(URL, data, HTTP_AUTHORIZATION=f"Bearer {token}")
    assert request.status_code == 422
    assert (
        request.data["message"]
        == "Create service failed. Fix the error(s) below"
    )


def test_update_service(client, generate_access_token1, create_service):
    """
    test update service
    """
    token, user = generate_access_token1
    URL = reverse("services:service", args=[create_service.id])
    data = {"name": "updated_one"}
    res = client.patch(
        URL,
        data,
        HTTP_AUTHORIZATION=f"Bearer {token}",
        content_type="application/json",
    )
    assert res.status_code == 200
    assert res.data["name"] == "updated_one"
