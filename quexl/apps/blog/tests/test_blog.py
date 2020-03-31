"""
test file for blogs
"""
import json

from django.urls import reverse


def test_listing_blog(
    client, generate_access_token1, create_blog, create_like, create_dislike
):
    """test for successful listing of blogs"""
    url = reverse("blog:blogs")
    token, _ = generate_access_token1
    response = client.get(url, HTTP_AUTHORIZATION=f"Bearer {token}")
    resp = json.loads(response.content.decode())
    assert response.status_code == 200
    assert resp["status"] == "success"


def test_retrieving_a_blog(client, generate_access_token1, create_blog):
    """test for successful retieving of a blog"""
    url = reverse("blog:blog", args=[create_blog.id])
    token, _ = generate_access_token1
    response = client.get(url, HTTP_AUTHORIZATION=f"Bearer {token}")
    resp = json.loads(response.content.decode())
    assert response.status_code == 200
    assert resp["status"] == "success"


def test_updating_a_blog(client, generate_access_token1, create_blog):
    """test for unsuccessful updating of a comment with an invalid move"""
    url = reverse("blog:blog", args=[create_blog.id])
    token, _ = generate_access_token1
    data = {"title": "This is the updated title"}
    response = client.patch(
        url,
        data=data,
        HTTP_AUTHORIZATION=f"Bearer {token}",
        content_type="application/json",
    )
    resp = json.loads(response.content.decode())
    assert response.status_code == 200
    assert resp["status"] == "success"
    assert resp["message"] == "Blog updated succesfully"


def test_creating_blog(client, generate_access_token1):
    """test for successful creation of blogs"""
    url = reverse("blog:blogs")
    token, _ = generate_access_token1
    data = {
        "title": "This is a blog",
        "short_description": "Lorem ipsum ",
        "description": "it amet, consectetur adipiscing elh",
        "body": "retium viverra. Iaculis urna id volutpat lacus laoreet n",
    }
    response = client.post(
        url, data=data, HTTP_AUTHORIZATION=f"Bearer {token}"
    )
    resp = json.loads(response.content.decode())
    assert response.status_code == 201
    assert resp["status"] == "success"
    assert resp["data"]["title"] == "This is a blog"
