from pydantic import BaseModel, ConfigDict


class ShopifyProductResponse(BaseModel):
    id: str
    title: str
    vendor: str | None = None
    status: str

    model_config = ConfigDict(from_attributes=True)
