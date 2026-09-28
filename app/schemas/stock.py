from datetime import datetime

from pydantic import BaseModel


class StockCreate(BaseModel):
    product_id: int
    quantity: int


class StockResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }