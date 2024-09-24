from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class ProductBase(BaseModel):
    title: str = Field(
        None,
        min_length=1,
        max_length=100,
        description='Название товара'
    )
    description: Optional[str] = None
    price: Decimal = Field(
        None,
        gt=0,
        decimal_places=2,
        max_digits=10,
        description='Цена товара'
    )
    quantity_in_warehouse: int = Field(
        None,
        ge=0,
        description='Количество товара на складе'
    )


class ProductCreate(ProductBase):
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description='Название товара'
    )
    price: Decimal = Field(
        ...,
        gt=0,
        decimal_places=2,
        max_digits=10,
        description='Цена товара'
    )
    quantity_in_warehouse: int = Field(
        ...,
        ge=0,
        description='Количество товара на складе'
    )


class ProductUpdate(ProductBase):

    @field_validator('title')
    def title_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Название товара не может быть пустым!')
        return value


class ProductBD(ProductCreate):
    id: int

    class Config:
        from_attributes = True
