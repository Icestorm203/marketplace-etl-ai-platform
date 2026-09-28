from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductUpdate
)

from app.services.product_service import (
    create_product,
    get_products,
    get_product_by_id,
    update_product,
    delete_product
)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post(
    "",
    response_model=ProductResponse
)
def create_product_endpoint(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    return create_product(db, product)


@router.get(
    "",
    response_model=list[ProductResponse]
)
def get_products_endpoint(
    db: Session = Depends(get_db)
):
    return get_products(db)


@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def get_product_by_id_endpoint(
    product_id: int,
    db: Session = Depends(get_db)
):
    return get_product_by_id(
        db,
        product_id
    )


@router.put(
    "/{product_id}",
    response_model=ProductResponse
)
def update_product_endpoint(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db)
):
    return update_product(
        db,
        product_id,
        product
    )


@router.delete("/{product_id}")
def delete_product_endpoint(
    product_id: int,
    db: Session = Depends(get_db)
):
    return delete_product(
        db,
        product_id
    )