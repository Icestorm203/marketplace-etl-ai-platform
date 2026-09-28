from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.stock import Stock
from app.schemas.stock import StockCreate


def create_stock(
    db: Session,
    stock_data: StockCreate
):
    stock = Stock(
        product_id=stock_data.product_id,
        quantity=stock_data.quantity
    )

    db.add(stock)
    db.commit()
    db.refresh(stock)

    return stock


def get_stocks(db: Session):
    return db.query(Stock).all()


def get_stock_by_id(
    db: Session,
    stock_id: int
):
    stock = db.get(Stock, stock_id)

    if stock is None:
        raise HTTPException(
            status_code=404,
            detail="Stock not found"
        )

    return stock