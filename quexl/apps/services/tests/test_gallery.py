import json

from django.urls import reverse


def test_list_gallery(client, generate_access_token1, create_gallery):
    """
    test listing gallery
    """
    URL = reverse("services:galleries")
    token, user = generate_access_token1
    response = client.get(URL, HTTP_AUTHORIZATION=f"Bearer {token}")
    resp = json.loads(response.content.decode())
    assert response.status_code == 200
    assert resp["status"] == "success"
    assert (
        resp["data"][0]["image"] == "http://testserver/api/test_images/img.jpg"
    )


def test_get_a_gallery(client, generate_access_token1, create_gallery):
    """
    test getting a gallery
    """
    URL = reverse("services:gallery", args=[create_gallery.id])
    token, user = generate_access_token1
    response = client.get(URL, HTTP_AUTHORIZATION=f"Bearer {token}")
    resp = json.loads(response.content.decode())
    assert response.status_code == 200
    assert resp["status"] == "success"
    assert (
        resp["data"]["image"]
        == "http://testserver/api/gallery/test_images/img.jpg"
    )


def test_create_gallery_with_invalid_service(client, generate_access_token1):
    """
    test getting a gallery with invalid service
    """
    token, user = generate_access_token1
    URL = reverse("services:galleries")
    data = {"image": "http://testserver/api/gallery/test_images/img.jpg"}
    data["service"] = "wrongservice"
    request = client.post(URL, data, HTTP_AUTHORIZATION=f"Bearer {token}")
    assert request.status_code == 422
    assert (
        request.data["message"]
        == "Create gallery failed. Fix the error(s) below"
    )


def test_update_gallery(client, generate_access_token1, create_gallery):
    """
    test update gallery
    """
    token, user = generate_access_token1
    URL = reverse("services:gallery", args=[create_gallery.id])
    data = {"description": "updated_one"}
    res = client.patch(
        URL,
        data,
        HTTP_AUTHORIZATION=f"Bearer {token}",
        content_type="application/json",
    )
    assert res.status_code == 200
    assert res.data["description"] == "updated_one"
