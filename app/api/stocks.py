from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.stock import (
    StockCreate,
    StockResponse
)

from app.services.stock_service import (
    create_stock,
    get_stocks,
    get_stock_by_id
)

router = APIRouter(
    prefix="/stocks",
    tags=["Stocks"]
)


@router.post(
    "",
    response_model=StockResponse
)
def create_stock_endpoint(
    stock: StockCreate,
    db: Session = Depends(get_db)
):
    return create_stock(db, stock)


@router.get(
    "",
    response_model=list[StockResponse]
)
def get_stocks_endpoint(
    db: Session = Depends(get_db)
):
    return get_stocks(db)


@router.get(
    "/{stock_id}",
    response_model=StockResponse
)
def get_stock_by_id_endpoint(
    stock_id: int,
    db: Session = Depends(get_db)
):
    return get_stock_by_id(
        db,
        stock_id
    )