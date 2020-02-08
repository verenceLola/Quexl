import json

from django.urls import reverse


def test_list_categories(client, generate_access_token1, create_category):
    """
    test listing categories
    """
    URL = reverse("services:categories")
    token, user = generate_access_token1
    response = client.get(URL, HTTP_AUTHORIZATION=f"Bearer {token}")
    resp = json.loads(response.content.decode())
    assert response.status_code == 200
    assert resp["status"] == "success"
    assert resp["data"][0]["name"] == create_category.name


def test_category2(client, generate_access_token1, create_category2):
    """
    test listing categories
    """
    URL = reverse("services:categories")
    token, user = generate_access_token1
    response = client.get(URL, HTTP_AUTHORIZATION=f"Bearer {token}")
    resp = json.loads(response.content.decode())
    assert response.status_code == 200
    assert resp["status"] == "success"
    assert resp["data"][0]["sub_categories"][0]["name"] == "sub_category"


def test_get_a_category(client, generate_access_token1, create_category):
    """
    test geting one category
    """
    URL = reverse("services:category", args=[create_category.id])
    token, user = generate_access_token1
    response = client.get(URL, HTTP_AUTHORIZATION=f"Bearer {token}")
    resp = json.loads(response.content.decode())
    assert response.status_code == 200
    assert resp["status"] == "success"
    assert resp["data"]["name"] == "category_one"


def test_create_category_with_errors(
    client, generate_access_token1, create_category
):
    """
    test getting a categories with errors
    """
    token, user = generate_access_token1
    URL = reverse("services:categories")
    data = {
        "name": "category_one",
    }
    data["parent_id"] = "invalid"
    request = client.post(URL, data, HTTP_AUTHORIZATION=f"Bearer {token}")
    assert request.status_code == 422
    assert (
        request.data["message"]
        == "create category failed. Fix the error(s) below"
    )


def test_create_existing_category(
    client, generate_access_token1, create_category
):
    """
    test creating duplicate category
    """
    token, user = generate_access_token1
    URL = reverse("services:categories")
    data = {"name": "category_one"}
    client.post(URL, data, HTTP_AUTHORIZATION=f"Bearer {token}")
    res = client.post(URL, data, HTTP_AUTHORIZATION=f"Bearer {token}")
    assert res.status_code == 422
    assert (
        res.data["message"] == "create category failed. Fix the error(s) below"
    )


def test_update_with_errors(
    client, generate_access_token1, create_category, create_category2
):
    """
    test update category
    """
    token, user = generate_access_token1
    URL = reverse("services:category", args=[create_category.id])
    data = {"name": "updated_one", "parent_id": create_category2.id}
    res = client.patch(
        URL,
        data,
        HTTP_AUTHORIZATION=f"Bearer {token}",
        content_type="application/json",
    )
    assert res.status_code == 422
    assert res.data["message"] == "category failed. Fix the error(s) below"


def test_creating_duplicate_categories(
    client, generate_access_token1, create_category
):
    """
    test creating duplicate category
    """
    token, user = generate_access_token1
    URL = reverse("services:categories")
    data = {"name": "category_one_new", "parent_id": create_category.id}
    client.post(URL, data, HTTP_AUTHORIZATION=f"Bearer {token}")
    res = client.post(URL, data, HTTP_AUTHORIZATION=f"Bearer {token}")
    assert res.status_code == 422
    assert (
        res.data["message"] == "create category failed. Fix the error(s) below"
    )


def test_update_category(client, generate_access_token1, create_category):
    """
    test update category
    """
    token, user = generate_access_token1
    URL = reverse("services:category", args=[create_category.id])
    data = {"name": "updated_one"}
    res = client.patch(
        URL,
        data,
        HTTP_AUTHORIZATION=f"Bearer {token}",
        content_type="application/json",
    )
    assert res.status_code == 200
    assert res.data["name"] == "updated_one"


def test_update_with_put_method(
    client, generate_access_token1, create_category
):
    """
    test update category
    """
    token, user = generate_access_token1
    URL = reverse("services:category", args=[create_category.id])
    data = {"name": "updated_one"}
    res = client.put(
        URL,
        data,
        HTTP_AUTHORIZATION=f"Bearer {token}",
        content_type="application/json",
    )
    assert res.status_code == 405
    assert res.data["message"] == "To update category, use PATCH method"


def test_delete_category(client, generate_access_token1, create_category3):
    """
    test delete category
    """
    token, user = generate_access_token1
    URL = reverse("services:category", args=[create_category3.id])
    res = client.delete(URL, HTTP_AUTHORIZATION=f"Bearer {token}")
    assert res.status_code == 200
    assert res.data == {}
