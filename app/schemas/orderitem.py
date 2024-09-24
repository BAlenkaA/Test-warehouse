from pydantic import BaseModel, Field


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., ge=1, description="Количество товара в заказе")

    class Config:
        from_attributes = True


class OrderItemDB(OrderItemCreate):
    id: int

    class Config:
        from_attributes = True
