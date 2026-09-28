from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.product import Product
from app.schemas.product import (
    ProductCreate,
    ProductUpdate
)

def create_product(
    db: Session,
    product_data: ProductCreate
):
    product = Product(
        sku=product_data.sku,
        name=product_data.name,
        purchase_price=product_data.purchase_price,
        sale_price=product_data.sale_price
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


def get_products(db: Session):
    return db.query(Product).all()


def get_product_by_id(
    db: Session,
    product_id: int
):
    product = db.get(Product, product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


def update_product(
    db: Session,
    product_id: int,
    product_data: ProductUpdate
):
    product = db.get(Product, product_id)

    if not product:
        return None

    product.sku = product_data.sku
    product.name = product_data.name
    product.purchase_price = product_data.purchase_price
    product.sale_price = product_data.sale_price

    db.commit()
    db.refresh(product)

    return product


def delete_product(
    db: Session,
    product_id: int
):
    product = db.get(Product, product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted"
    }
