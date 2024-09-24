from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_inventory, check_order_exists,
                                check_product_exists)
from app.crud.base import CRUDBase
from app.models.order import Order, OrderItem
from app.schemas.order import OrderCreate


class CDUROrder(CRUDBase):
    """
    Класс для CRUD-операций модели Order.
    """

    @staticmethod
    async def create(
            new_order: OrderCreate,
            session: AsyncSession,
    ) -> Order:
        db_order = Order(status=new_order.status)
        session.add(db_order)

        for item in new_order.items:
            await check_product_exists(item.product_id, session)
            product = await check_inventory(item, session)
            product.quantity_in_warehouse -= item.quantity
            db_order_item = OrderItem(
                product_id=item.product_id,
                order_id=db_order.id,
                quantity=item.quantity
            )
            session.add(db_order_item)
        await session.commit()
        await session.refresh(db_order)
        return db_order

    @staticmethod
    async def update_status(
            order_id: int,
            new_status: str,
            session: AsyncSession,
    ) -> Order:
        order = await check_order_exists(order_id, session)
        order.status = new_status
        await session.commit()
        await session.refresh(order)

        return order


order_crud = CDUROrder(Order)
