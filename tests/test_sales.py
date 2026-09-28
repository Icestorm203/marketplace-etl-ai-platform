def test_create_sale(client, product):
    response = client.post(
        "/sales",
        json={
            "product_id": product["id"],
            "quantity": 3,
            "sale_amount": 2970
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] > 0
    assert data["product_id"] == product["id"]
    assert data["quantity"] == 3
    assert data["sale_amount"] == 2970


def test_get_sales(client, product):
    client.post(
        "/sales",
        json={
            "product_id": product["id"],
            "quantity": 2,
            "sale_amount": 1980
        }
    )

    response = client.get("/sales")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_sale_by_id(client, product):
    create_response = client.post(
        "/sales",
        json={
            "product_id": product["id"],
            "quantity": 1,
            "sale_amount": 990
        }
    )

    sale_id = create_response.json()["id"]

    response = client.get(f"/sales/{sale_id}")

    assert response.status_code == 200
    assert response.json()["sale_amount"] == 990


def test_get_missing_sale(client):
    response = client.get("/sales/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Sale not found"
    }