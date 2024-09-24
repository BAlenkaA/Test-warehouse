from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.product import product_crud
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductBD, ProductUpdate

router = APIRouter(prefix='/products', tags=['Products'])


@router.post(
    '/',
    response_model=ProductBD,
    response_model_exclude_none=True,
)
async def create_new_product(
        product: ProductCreate,
        session: AsyncSession = Depends(get_async_session)
):
    await check_title_duplicate(product.title, session)
    new_product = await product_crud.create(product, session)
    return new_product


@router.get(
    '/',
    response_model=list[ProductBD],
    response_model_exclude_none=True,
)
async def get_all_products(
        session: AsyncSession = Depends(get_async_session)
):
    all_products = await product_crud.get_multi(session)
    return all_products


@router.get(
    '/{id}',
    response_model=ProductBD,
    response_model_exclude_none=True,
)
async def get_product(
        id: int,
        session: AsyncSession = Depends(get_async_session)
):
    product = await check_product_exists(id, session)
    return product


@router.put(
    '/{id}',
    response_model=ProductBD,
    response_model_exclude_none=True,
)
async def full_update_product(
        id: int,
        obj_in: ProductUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    product = await check_product_exists(id, session)
    await check_title_duplicate(obj_in.title, session, id)
    product = await product_crud.update_product(product, obj_in, session)
    return product


@router.delete(
    '/{id}',
    response_model=ProductBD,
    response_model_exclude_none=True,
)
async def remote_product(
        id: int,
        session: AsyncSession = Depends(get_async_session)
):
    product = await check_product_exists(id, session)
    product = await product_crud.delete_product(product, session)
    return product


async def check_title_duplicate(
        product_title: str,
        session: AsyncSession,
        current_product_id: int | None = None
) -> None:
    product_id = await product_crud.get_product_id_by_title(product_title, session)
    if product_id is not None and product_id != current_product_id:
        raise HTTPException(
            status_code=422,
            detail='Товар с таким названием уже существует!',
        )


async def check_product_exists(
        product_id: int,
        session: AsyncSession,
) -> Product:
    product = await product_crud.get(product_id, session)
    if product is None:
        raise HTTPException(
            status_code=404,
            detail='Товар не найден!'
        )
    return product
