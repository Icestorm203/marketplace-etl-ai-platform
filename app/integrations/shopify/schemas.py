from pydantic import BaseModel
from pydantic import Field


class ShopifyProduct(BaseModel):
    id: str
    title: str
    vendor: str | None = None
    status: str


class ShopifyPageInfo(BaseModel):
    has_next_page: bool = Field(
        validation_alias="hasNextPage"
    )

    end_cursor: str | None = Field(
        default=None,
        validation_alias="endCursor"
    )


class ShopifyProductsPage(BaseModel):
    products: list[ShopifyProduct]
    page_info: ShopifyPageInfo


class ShopifyProductsResponse(BaseModel):
    products: ShopifyProductsPage