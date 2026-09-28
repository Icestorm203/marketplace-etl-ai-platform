from datetime import datetime

from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import func

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from typing import List

from app.database.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    sku: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    purchase_price: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    sale_price: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    stocks: Mapped[List["Stock"]] = relationship(
        back_populates="product"
    )

    sales: Mapped[List["Sale"]] = relationship(
        back_populates="product"
    )