from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_order_exists
from app.core.db import get_async_session
from app.crud.order import order_crud
from app.schemas.order import OrderCreate, OrderDB, OrderStatusUpdate

router = APIRouter()


@router.post(
    '/',
    response_model=OrderDB,
    response_model_exclude_none=True,
)
async def create_new_order(
        order: OrderCreate,
        session: AsyncSession = Depends(get_async_session)
):
    new_order = await order_crud.create(order, session)
    return new_order


@router.get(
    '/',
    response_model=list[OrderDB],
    response_model_exclude_none=True,
)
async def get_all_orders(
        session: AsyncSession = Depends(get_async_session)
):
    all_orders = await order_crud.get_multi(session)
    return all_orders


@router.get(
    '/{id}',
    response_model=OrderDB,
    response_model_exclude_none=True,
)
async def get_order(
        id: int,
        session: AsyncSession = Depends(get_async_session)
):
    order = await check_order_exists(id, session)
    return order


@router.patch(
    '/{id}/status',
    response_model=OrderDB,
    response_model_exclude_none=True,
)
async def update_order_status(
        id: int,
        status_update: OrderStatusUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    order = await order_crud.update_status(id, status_update.status, session)
    return order
