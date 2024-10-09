import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings, DATABASE_URL
from app.core.db import Base, get_async_session
from app.main import app
from app.models import Product, Order
from app.models.order import OrderStatus, OrderItem

engine_test = create_async_engine(DATABASE_URL, future=True)
AsyncSessionTest = sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = engine_test


async def override_get_async_session():
    async with AsyncSessionTest() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session


@pytest_asyncio.fixture(scope='session')
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture(scope='session', autouse=True)
async def create_test_db():
    assert settings.mode == "TEST"
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def populate_products():
    async with AsyncSessionTest() as session:
        product_data = [
            Product(title="Product 1", description="First product", price=10.0, quantity_in_warehouse=50),
            Product(title="Product 2", description="Second product", price=20.0, quantity_in_warehouse=30),
            Product(title="Product 3", price=30.0, quantity_in_warehouse=20),
        ]
        session.add_all(product_data)
        await session.commit()


@pytest_asyncio.fixture
async def populate_orders():
    async with AsyncSessionTest() as session:
        order_data = [
            Order(status=OrderStatus.shipped, items=[
                OrderItem(product_id=1, quantity=5),
                OrderItem(product_id=2, quantity=3)
            ]),
            Order(status=OrderStatus.shipped, items=[
                OrderItem(product_id=1, quantity=2)
            ]),
            Order(status=OrderStatus.shipped, items=[
                OrderItem(product_id=2, quantity=1)
            ])
        ]
        session.add_all(order_data)
        await session.commit()
