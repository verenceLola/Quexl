"""
test file for comments
"""
import json

from django.urls import reverse


def test_listing_comments(client, generate_access_token1, create_comment):
    """test for successful listing of comments"""
    url = reverse("blog:comments")
    token, _ = generate_access_token1
    response = client.get(url, HTTP_AUTHORIZATION=f"Bearer {token}")
    resp = json.loads(response.content.decode())
    assert response.status_code == 200
    assert resp["status"] == "success"


def test_retrieving_a_comment(client, generate_access_token1, create_comment):
    """test for successful retrieving of a comment"""
    url = reverse("blog:comment", args=[create_comment.id])
    token, _ = generate_access_token1
    response = client.get(url, HTTP_AUTHORIZATION=f"Bearer {token}")
    resp = json.loads(response.content.decode())
    assert response.status_code == 200
    assert resp["status"] == "success"


def test_updating_a_comment(
    client, generate_access_token1, create_comment, create_subcomment
):
    """test for unsuccessful updating of a comment with an invalid move"""
    url = reverse("blog:comment", args=[create_comment.id])
    token, _ = generate_access_token1
    data = {
        "body": "This is the updated comment body",
        "parent_id": create_subcomment.id,
    }
    response = client.patch(
        url,
        data=data,
        HTTP_AUTHORIZATION=f"Bearer {token}",
        content_type="application/json",
    )
    resp = json.loads(response.content.decode())
    assert response.status_code == 422
    assert resp["status"] == "error"


def test_creating_comments(
    client, generate_access_token1, create_comment, create_blog
):
    """test for successful creation of comments"""
    url = reverse("blog:comments")
    token, _ = generate_access_token1
    data = {
        "blog": create_blog.id,
        "body": "This is the comment body",
        "parent_id": create_comment.id,
    }
    response = client.post(
        url, data=data, HTTP_AUTHORIZATION=f"Bearer {token}"
    )
    resp = json.loads(response.content.decode())
    assert response.status_code == 201
    assert resp["status"] == "success"
    assert resp["data"]["body"] == "This is the comment body"
