from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from app.models.order import OrderStatus
from app.schemas.orderitem import OrderItemCreate


class OrderStatusUpdate(BaseModel):
    status: OrderStatus

    class Config:
        use_enum_values = True


class OrderCreate(OrderStatusUpdate):
    items: List[OrderItemCreate] = Field(
        ...,
        description='Список элементов заказа'
    )


class OrderDB(OrderCreate):
    id: int
    date_create: datetime

    class Config:
        from_attributes = True
