import enum
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class OrderStatus(enum.Enum):
    in_progress = 'in_progress'
    shipped = 'shipped'
    delivered = 'delivered'


class Order(Base):
    date_create: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus), nullable=False)
    items: Mapped[list['OrderItem']] = relationship(
        back_populates='order',
        lazy='selectin',
        cascade='all, delete-orphan'
    )


class OrderItem(Base):
    order_id: Mapped[int] = mapped_column(ForeignKey('order.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    quantity: Mapped[int]
    __table_args__ = (
        CheckConstraint('quantity > 0', name='check_quantity_positive'),)
    order: Mapped['Order'] = relationship(
        back_populates='items'
    )
    product: Mapped['Product'] = relationship(
        back_populates='order_items'
    )
