from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.sale import Sale
    from app.models.stock import Stock

from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    sku: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    purchase_price: Mapped[float] = mapped_column(Float, nullable=False)

    sale_price: Mapped[float] = mapped_column(Float, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    stocks: Mapped[list["Stock"]] = relationship(back_populates="product")

    sales: Mapped[list["Sale"]] = relationship(back_populates="product")
