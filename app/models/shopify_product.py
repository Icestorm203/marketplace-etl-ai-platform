from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database.database import Base


class ShopifyProduct(Base):
    __tablename__ = "shopify_products"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    vendor: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )