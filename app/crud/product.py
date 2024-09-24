from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class CRUDProduct(CRUDBase):
    """
    Класс для CRUD-операций модели Product.
    """

    @staticmethod
    async def create(
            new_product: ProductCreate,
            session: AsyncSession,
    ) -> Product:
        new_product_data = new_product.model_dump()
        db_product = Product(**new_product_data)
        session.add(db_product)
        await session.commit()
        await session.refresh(db_product)
        return db_product

    @staticmethod
    async def update_product(
            db_product: Product,
            product_in: ProductUpdate,
            session: AsyncSession,
    ) -> Product:
        for field, value in product_in.model_dump().items():
            setattr(db_product, field, value)
        session.add(db_product)
        await session.commit()
        await session.refresh(db_product)
        return db_product

    @staticmethod
    async def delete_product(
            db_product: Product,
            session: AsyncSession,
    ) -> Product:
        await session.delete(db_product)
        await session.commit()
        return db_product

    @staticmethod
    async def get_product_id_by_title(
            product_title: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_product_id = await session.execute(
            select(Product.id).where(
                Product.title == product_title
            )
        )
        db_product_id = db_product_id.scalars().first()
        return db_product_id


product_crud = CRUDProduct(Product)
