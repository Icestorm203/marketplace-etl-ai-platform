def test_create_stock(client, product):
    response = client.post(
        "/stocks",
        json={
            "product_id": product["id"],
            "quantity": 100
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] > 0
    assert data["product_id"] == product["id"]
    assert data["quantity"] == 100


def test_get_stock_by_id(client, product):
    create_response = client.post(
        "/stocks",
        json={
            "product_id": product["id"],
            "quantity": 50
        }
    )

    stock_id = create_response.json()["id"]

    response = client.get(f"/stocks/{stock_id}")

    assert response.status_code == 200
    assert response.json()["quantity"] == 50


def test_get_missing_stock(client):
    response = client.get("/stocks/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Stock not found"
    }