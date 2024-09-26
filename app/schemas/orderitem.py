from pydantic import BaseModel, ConfigDict, Field


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., ge=1, description="Количество товара в заказе")

    model_config = ConfigDict(
        from_attributes=True
    )


class OrderItemDB(OrderItemCreate):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )
