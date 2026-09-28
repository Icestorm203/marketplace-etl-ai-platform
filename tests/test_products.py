def test_create_product(client):
    response = client.post(
        "/products",
        json={
            "sku": "SKU-CREATE",
            "name": "Mouse",
            "purchase_price": 500,
            "sale_price": 990
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] > 0
    assert data["sku"] == "SKU-CREATE"
    assert data["name"] == "Mouse"
    assert data["purchase_price"] == 500
    assert data["sale_price"] == 990
    assert data["created_at"] is not None


def test_get_products(client, product):
    response = client.get("/products")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["id"] == product["id"]


def test_get_product_by_id(client, product):
    response = client.get(
        f"/products/{product['id']}"
    )

    assert response.status_code == 200
    assert response.json()["sku"] == "TEST-SKU-001"


def test_get_missing_product(client):
    response = client.get("/products/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Product not found"
    }


def test_update_product(client, product):
    response = client.put(
        f"/products/{product['id']}",
        json={
            "sku": "TEST-SKU-UPDATED",
            "name": "Gaming Mouse",
            "purchase_price": 600,
            "sale_price": 1190
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["sku"] == "TEST-SKU-UPDATED"
    assert data["name"] == "Gaming Mouse"
    assert data["sale_price"] == 1190


def test_delete_product(client, product):
    response = client.delete(
        f"/products/{product['id']}"
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Product deleted"
    }

    get_response = client.get(
        f"/products/{product['id']}"
    )

    assert get_response.status_code == 404


def test_delete_missing_product(client):
    response = client.delete("/products/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Product not found"
    }