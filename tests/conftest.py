import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.db import Base, get_async_session
from app.main import app

DATABASE_URL_TEST = (f'postgresql+asyncpg://{settings.db_user_test}:'
                     f'{settings.db_password_test}@{settings.db_host_test}:'
                     f'{settings.db_port_test}/{settings.db_name_test}')

engine_test = create_async_engine(DATABASE_URL_TEST, future=True)
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
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
