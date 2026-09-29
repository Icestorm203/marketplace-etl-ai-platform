from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.services.shopify_service import (
    sync_products,
    get_products,
    get_products_stats
)

from app.schemas.shopify_product import ShopifyProductResponse


router = APIRouter(
    prefix="/shopify",
    tags=["Shopify"]
)


@router.post("/products/sync")
def sync_shopify_products(
    db: Session = Depends(get_db)
):
    imported = sync_products(db)

    return {
        "imported": imported
    }


@router.get(
    "/products",
    response_model=list[ShopifyProductResponse]
)
def get_shopify_products(
    db: Session = Depends(get_db),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    return get_products(
        db=db,
        limit=limit,
        offset=offset
    )


@router.get("/products/stats")
def get_shopify_products_stats(
    db: Session = Depends(get_db)
):
    return get_products_stats(db)