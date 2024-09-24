from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.product import product_crud
from app.models.order import Order
from app.models.product import Product
from app.schemas.orderitem import OrderItemCreate


async def check_title_duplicate(
        product_title: str,
        session: AsyncSession,
        current_product_id: int | None = None
) -> None:
    """Проверка на уникальность названия продукта."""
    product_id = await product_crud.get_product_id_by_title(
        product_title, session)
    if product_id is not None and product_id != current_product_id:
        raise HTTPException(
            status_code=422,
            detail='Товар с таким названием уже существует!',
        )


async def check_exists(
        model,
        object_id: int,
        session: AsyncSession,
        error_message: str
):
    """Проверка, существует ли объект в базе данных."""
    result = await session.execute(select(model).filter_by(id=object_id))
    obj = result.scalars().first()

    if obj is None:
        raise HTTPException(
            status_code=404,
            detail=error_message
        )
    return obj


async def check_product_exists(
        product_id: int,
        session: AsyncSession,
) -> Product:
    """Проверка, существует ли продукт с данным ID."""
    return await check_exists(Product, product_id, session, 'Товар не найден!')


async def check_order_exists(
        order_id: int,
        session: AsyncSession,
) -> Order:
    """Проверка, существует ли заказ с данным ID."""
    return await check_exists(Order, order_id, session, 'Заказ не найден!')


async def check_inventory(
        item: OrderItemCreate,
        session: AsyncSession
):
    """
    Валидация наличия достаточного количества товара на складе.
    """
    product = await session.get(Product, item.product_id)
    if product.quantity_in_warehouse < item.quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Недостаточно товара на складе"
                   f" для продукта с ID {item.product_id}"
        )
    return product
