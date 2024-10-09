import pytest
import pytest_asyncio
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from contextlib import nullcontext as does_not_raise

from app.crud.product import product_crud
from app.models import Product
from app.schemas.product import ProductUpdate, ProductCreate
from tests.conftest import AsyncSessionTest


@pytest_asyncio.fixture
async def product_session():
    async with AsyncSessionTest() as session:
        yield session


@pytest.mark.asyncio(loop_scope='session')
@pytest.mark.parametrize(
    "title, description, price, quantity_in_warehouse, expectation",
    [
        ("Valid Product1", "A valid product description", 10.00, 5, does_not_raise()),
        ("Valid Product2", None, 10.00, 5, does_not_raise()),
        ("Unique Product", "A valid product with quantity_in_warehouse = 0", 10.00, 0, does_not_raise()),
        (None, "Invalid product without_title", 10.00, 5, pytest.raises(ValidationError)),
        ("Invalid Price Product4", "Product with negative price", -10.00, 5, pytest.raises(ValidationError)),
        ("Invalid Price Product5", "Product with negative quantity", 10.00, -5, pytest.raises(ValidationError)),
    ]
)
async def test_create_product(product_session, title, description, price, quantity_in_warehouse, expectation):
    with expectation:
        ProductCreate(title=title, description=description, price=price,
                                quantity_in_warehouse=quantity_in_warehouse)


@pytest.mark.asyncio(loop_scope='session')
@pytest.mark.parametrize(
    "title, description, price, quantity_in_warehouse, expectation",
    [
        ("Valid Updated Product1", "Updated description", 15.00, 10, does_not_raise()),
        ("Valid Updated Product2", "A valid update product with quantity_in_warehouse = 0", 15.00, 0, does_not_raise()),
        ("Valid Updated Product3", None, 15.00, 10, does_not_raise()),
        (None, "Updated description", 15.00, 10, pytest.raises(ValidationError)),
        ("Invalid Updated Product", "Updated product with negative price", -10.00, 10, pytest.raises(ValidationError)),
        ("Invalid Updated Product", "Updated product with negative quantity", 15.00, -5, pytest.raises(ValidationError)),
    ]
)
async def test_product_update_validation(product_session, title, description, price, quantity_in_warehouse, expectation):
    with expectation:
        ProductUpdate(
            title=title,
            description=description,
            price=price,
            quantity_in_warehouse=quantity_in_warehouse
        )


@pytest.mark.asyncio(loop_scope='session')
@pytest.mark.parametrize(
    "title, description, price, quantity_in_warehouse",
    [
        ("Valid Updated Product1", "Updated description", 15.00, 10),
        ("Valid Updated Product2", "A valid update product with quantity_in_warehouse = 0", 15.00, 0),
        ("Valid Updated Product3", None, 15.00, 10),  # Описание может быть None
    ]
)
async def test_update_product_in_db(product_session, title, description, price, quantity_in_warehouse):
    product = Product(title="Original Product", description="Original description", price=10.00, quantity_in_warehouse=5)
    product_session.add(product)
    await product_session.commit()

    product_in = ProductUpdate(
        title=title,
        description=description,
        price=price,
        quantity_in_warehouse=quantity_in_warehouse
    )

    updated_product = await product_crud.update_product(product, product_in, product_session)

    assert updated_product.title == title
    assert updated_product.description == description
    assert updated_product.price == price
    assert updated_product.quantity_in_warehouse == quantity_in_warehouse


@pytest.mark.asyncio(loop_scope='session')
async def test_delete_product_in_db(product_session):
    product = Product(title="Removed Product", description="Removed product description", price=10.00,
                      quantity_in_warehouse=5)
    product_session.add(product)
    await product_session.commit()

    product_from_db = await product_session.get(Product, product.id)
    assert product_from_db is not None

    await product_crud.delete_product(product_from_db, product_session)

    deleted_product = await product_session.get(Product, product.id)
    assert deleted_product is None