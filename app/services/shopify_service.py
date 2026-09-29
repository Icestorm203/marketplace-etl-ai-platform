from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.shopify_product import ShopifyProduct
from app.integrations.shopify.service import load_all_products



def sync_products(db: Session) -> int:
    products = load_all_products()

    imported = 0

    for product in products:

        existing = db.get(
            ShopifyProduct,
            product.id
        )

        if existing:
            existing.title = product.title
            existing.vendor = product.vendor
            existing.status = product.status
        else:
            db.add(
                ShopifyProduct(
                    id=product.id,
                    title=product.title,
                    vendor=product.vendor,
                    status=product.status,
                )
            )

        imported += 1

    db.commit()

    return imported


def get_products(
    db: Session,
    limit: int = 20,
    offset: int = 0
) -> list[ShopifyProduct]:
    return (
        db.query(ShopifyProduct)
        .order_by(ShopifyProduct.title)
        .offset(offset)
        .limit(limit)
        .all()
    )


def get_products_stats(db: Session) -> dict:
    total = db.query(
        func.count(ShopifyProduct.id)
    ).scalar()

    active = db.query(
        func.count(ShopifyProduct.id)
    ).filter(
        ShopifyProduct.status == "ACTIVE"
    ).scalar()

    draft = db.query(
        func.count(ShopifyProduct.id)
    ).filter(
        ShopifyProduct.status == "DRAFT"
    ).scalar()

    archived = db.query(
        func.count(ShopifyProduct.id)
    ).filter(
        ShopifyProduct.status == "ARCHIVED"
    ).scalar()

    return {
        "total_products": total,
        "active_products": active,
        "draft_products": draft,
        "archived_products": archived,
    }