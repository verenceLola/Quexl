"""
test file for likes
"""
import json

import pytest
from django.urls import reverse


def test_listing_like(client, generate_access_token1, create_like):
    """test for successful listing of likes"""
    url = reverse("blog:likes")
    token, _ = generate_access_token1
    response = client.get(url, HTTP_AUTHORIZATION=f"Bearer {token}")
    resp = json.loads(response.content.decode())
    assert response.status_code == 200
    assert resp["status"] == "success"


def test_creating_like(client, generate_access_token1, create_blog):
    """test for successful creation of likes"""
    url = reverse("blog:likes")
    token, _ = generate_access_token1
    data = {"blog": create_blog.id}
    response = client.post(
        url, data=data, HTTP_AUTHORIZATION=f"Bearer {token}"
    )
    resp = json.loads(response.content.decode())
    assert response.status_code == 201
    assert resp["status"] == "success"
    assert resp["message"] == "Blog like created successfully"


@pytest.mark.django_db(transaction=True)
def test_toggle_creating_like(
    client, generate_access_token1, create_blog, create_like
):
    """test for unsuccessful toggle creation of likes"""
    url = reverse("blog:likes")
    token, _ = generate_access_token1
    data = {"blog": create_blog.id}
    response = client.post(
        url, data=data, HTTP_AUTHORIZATION=f"Bearer {token}"
    )
    resp = json.loads(response.content.decode())
    assert response.status_code == 404
    assert resp["status"] == "error"
    assert resp["data"]["detail"] == "Like not found"
