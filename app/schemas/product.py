from datetime import datetime

from pydantic import BaseModel


class ProductCreate(BaseModel):
    sku: str
    name: str
    purchase_price: float
    sale_price: float


class ProductResponse(BaseModel):
    id: int
    sku: str
    name: str
    purchase_price: float
    sale_price: float
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class ProductUpdate(BaseModel):
    sku: str
    name: str
    purchase_price: float
    sale_price: float