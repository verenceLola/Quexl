"""
test file for orders
"""
import json

from django.urls import reverse


def test_list_contact_messages(client, generate_access_token1, create_contact):
    """test listing of contact messages"""
    url = reverse("contact:contacts")
    token, _ = generate_access_token1
    response = client.get(url, HTTP_AUTHORIZATION=f"Bearer {token}")
    resp = json.loads(response.content.decode())
    assert resp["data"][0]["full_name"] == "James Mwangi"
    assert response.status_code == 200
    assert resp["status"] == "success"


def test_retrieve_contact(client, generate_access_token1, create_contact):
    """test listing of contact messages"""
    url = reverse("contact:contact", args=[create_contact.id])
    token, _ = generate_access_token1
    response = client.get(url, HTTP_AUTHORIZATION=f"Bearer {token}")
    resp = json.loads(response.content.decode())
    assert resp["data"]["full_name"] == "James Mwangi"
    assert response.status_code == 200
    assert resp["status"] == "success"


def test_delete_contact(client, generate_access_token1, create_contact):
    """test listing of contact messages"""
    url = reverse("contact:contact", args=[create_contact.id])
    token, _ = generate_access_token1
    response = client.delete(url, HTTP_AUTHORIZATION=f"Bearer {token}")
    resp = json.loads(response.content.decode())
    assert resp["data"] == {}
    assert response.status_code == 200
    assert resp["status"] == "success"


def test_create_contact_with_errors(client, generate_access_token1):
    """test listing of contact messages"""
    url = reverse("contact:contacts")
    token, _ = generate_access_token1
    data = {
        "email": "tim@app.com",
        "subject": "Hey",
        "message": "I swear I hate your life even if it ain't mine",
    }
    response = client.post(
        url, data=data, HTTP_AUTHORIZATION=f"Bearer {token}"
    )
    resp = json.loads(response.content.decode())
    assert resp["message"] == "Correct the errors below"
    assert response.status_code == 422
    assert resp["status"] == "error"
