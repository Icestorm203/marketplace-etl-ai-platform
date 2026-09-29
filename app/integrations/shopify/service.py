from app.integrations.shopify.client import ShopifyClient
from app.integrations.shopify.schemas import (
    ShopifyProductsPage,
    ShopifyProductsResponse,
)


def load_products_page(
    limit: int = 50,
    cursor: str | None = None,
) -> ShopifyProductsPage:
    client = ShopifyClient()

    raw_data = client.get_products(
        first=limit,
        after=cursor,
    )

    validated = ShopifyProductsResponse.model_validate({
        "products": {
            "products": raw_data["products"]["nodes"],
            "page_info": raw_data["products"]["pageInfo"],
        }
    })

    return validated.products


def load_all_products() -> list:
    client = ShopifyClient()

    products = []
    cursor = None

    while True:
        raw_data = client.get_products(
            first=50,
            after=cursor,
        )

        page = raw_data["products"]

        products.extend(page["nodes"])

        if not page["pageInfo"]["hasNextPage"]:
            break

        cursor = page["pageInfo"]["endCursor"]

    validated = ShopifyProductsResponse.model_validate({
        "products": {
            "products": products,
            "page_info": {
                "hasNextPage": False,
                "endCursor": cursor,
            },
        }
    })

    return validated.products.products