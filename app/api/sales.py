from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.sale import (
    SaleCreate,
    SaleResponse
)

from app.services.sale_service import (
    create_sale,
    get_sales,
    get_sale_by_id
)

router = APIRouter(
    prefix="/sales",
    tags=["Sales"]
)


@router.post(
    "",
    response_model=SaleResponse
)
def create_sale_endpoint(
    sale: SaleCreate,
    db: Session = Depends(get_db)
):
    return create_sale(db, sale)


@router.get(
    "",
    response_model=list[SaleResponse]
)
def get_sales_endpoint(
    db: Session = Depends(get_db)
):
    return get_sales(db)


@router.get(
    "/{sale_id}",
    response_model=SaleResponse
)
def get_sale_by_id_endpoint(
    sale_id: int,
    db: Session = Depends(get_db)
):
    return get_sale_by_id(
        db,
        sale_id
    )