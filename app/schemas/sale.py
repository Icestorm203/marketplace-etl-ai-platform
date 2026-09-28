from pydantic import BaseModel


class SaleCreate(BaseModel):
    product_id: int
    quantity: int
    sale_amount: float


class SaleResponse(SaleCreate):
    id: int

    model_config = {
        "from_attributes": True
    }