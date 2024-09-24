from sqlalchemy import DECIMAL, CheckConstraint, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Product(Base):
    title: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    price: Mapped[DECIMAL] = mapped_column(DECIMAL(precision=10, scale=2))
    quantity_in_warehouse: Mapped[int]
    __table_args__ = (
        CheckConstraint(
            'quantity_in_warehouse >= 0',
            name='check_quantity_in_warehouse_greater_or_equal_to_0'
        ),
        CheckConstraint('price > 0', name='check_price_positive')
    )
    order_items: Mapped[list['OrderItem']] = relationship(
        back_populates='product',
        cascade='all, delete-orphan'
    )
