from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.sale import Sale
from app.schemas.sale import SaleCreate


def create_sale(
    db: Session,
    sale_data: SaleCreate
) -> Sale:

    sale = Sale(
        product_id=sale_data.product_id,
        quantity=sale_data.quantity,
        sale_amount=sale_data.sale_amount
    )

    db.add(sale)
    db.commit()
    db.refresh(sale)

    return sale


def get_sales(db: Session):
    return db.query(Sale).all()


def get_sale_by_id(
    db: Session,
    sale_id: int
):
    sale = db.get(Sale, sale_id)

    if not sale:
        raise HTTPException(
            status_code=404,
            detail="Sale not found"
        )

    return sale