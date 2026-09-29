from app.integrations.shopify.schemas import (
    ShopifyProduct
)


def test_get_shopify_products(
    client
):
    response = client.get(
        "/shopify/products"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(
        data,
        list
    )


def test_get_shopify_products_pagination(
    client
):
    response = client.get(
        "/shopify/products?limit=5&offset=0"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) <= 5


def test_get_shopify_products_stats(
    client
):
    response = client.get(
        "/shopify/products/stats"
    )

    assert response.status_code == 200

    data = response.json()

    assert "total_products" in data
    assert "active_products" in data
    assert "draft_products" in data
    assert "archived_products" in data


def test_sync_shopify_products(
    client,
    monkeypatch
):
    fake_products = [
        ShopifyProduct(
            id="gid://shopify/Product/1",
            title="Test Product",
            vendor="Test Vendor",
            status="ACTIVE"
        ),
        ShopifyProduct(
            id="gid://shopify/Product/2",
            title="Draft Product",
            vendor=None,
            status="DRAFT"
        ),
    ]

    monkeypatch.setattr(
        "app.services.shopify_service.load_all_products",
        lambda: fake_products
    )

    response = client.post(
        "/shopify/products/sync"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["imported"] == 2