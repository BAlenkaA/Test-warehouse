import pytest
from httpx import AsyncClient


def float_to_str(data_float):
    return f"{float(data_float['price']):.2f}"


@pytest.mark.asyncio(loop_scope='session')
async def test_create_product(async_client: AsyncClient):
    """
    Тест на создание нового продукта.
    """
    product_data = {
        "title": "New Product",
        "description": "A test product",
        "price": 99.99,
        "quantity_in_warehouse": 100
    }
    response = await async_client.post("/products/", json=product_data)
    assert response.status_code == 200
    data = response.json()
    #
    assert data["title"] == product_data["title"]
    assert data["description"] == product_data["description"]
    assert data["price"] == float_to_str(product_data)
    assert (data["quantity_in_warehouse"] ==
            product_data["quantity_in_warehouse"])
    assert "id" in data


@pytest.mark.asyncio(loop_scope='session')
async def test_get_all_products(async_client: AsyncClient):
    """
    Тест на получение всех продуктов.
    """
    response = await async_client.get("/products/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  # Должен вернуться список
    assert len(data) > 0  # Список не должен быть пустым, если есть продукты


@pytest.mark.asyncio(loop_scope='session')
async def test_get_product_by_id(async_client: AsyncClient):
    """
    Тест на получение продукта по ID.
    """

    response = await async_client.get("/products/1")
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == 1
    assert data["title"] == "New Product"
    assert data["description"] == "A test product"
    assert data["price"] == '99.99'
    assert data["quantity_in_warehouse"] == 100


@pytest.mark.asyncio(loop_scope='session')
async def test_update_product(async_client: AsyncClient):
    """
    Тест на обновление продукта.
    """
    update_data = {
        "title": "Updated Product",
        "description": "Updated description",
        "price": 150.00,
        "quantity_in_warehouse": 200
    }
    response = await async_client.put("/products/1", json=update_data)
    assert response.status_code == 200
    data = response.json()

    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]
    assert data["price"] == float_to_str(update_data)
    assert (data["quantity_in_warehouse"] ==
            update_data["quantity_in_warehouse"])


@pytest.mark.asyncio(loop_scope='session')
async def test_delete_product(async_client: AsyncClient):
    """
    Тест на удаление продукта.
    """
    response = await async_client.get("/products/")
    data = response.json()
    count_before = len(data)

    response = await async_client.delete("/products/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

    response = await async_client.get("/products/")
    data = response.json()
    count_after = len(data)
    assert count_after == count_before - 1
