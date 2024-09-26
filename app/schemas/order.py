from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, Field

from app.models.order import OrderStatus
from app.schemas.orderitem import OrderItemCreate


class OrderStatusUpdate(BaseModel):
    status: OrderStatus

    model_config = ConfigDict(
        use_enum_values=True
    )


class OrderCreate(OrderStatusUpdate):
    items: List[OrderItemCreate] = Field(
        ...,
        description='Список элементов заказа'
    )


class OrderDB(OrderCreate):
    id: int
    date_create: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
