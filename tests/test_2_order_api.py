import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(loop_scope='session')
async def test_create_order(async_client: AsyncClient):
    """
    Тест на создание нового заказа.
    """
    order_data = {
        "status": "in_progress",
        "items": [
            {"product_id": 1, "quantity": 5},
            {"product_id": 2, "quantity": 3},
            {"product_id": 3, "quantity": 2}
        ]
    }
    response = await async_client.post("/orders/", json=order_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "in_progress"
    assert len(data["items"]) == 3
    assert "id" in data

    for item, expected_item in zip(data["items"], order_data["items"]):
        assert item["product_id"] == expected_item["product_id"]
        assert item["quantity"] == expected_item["quantity"]


@pytest.mark.asyncio(loop_scope='session')
async def test_get_all_orders(async_client: AsyncClient, populate_orders):
    """
    Тест на получение всех заказов.
    """

    response = await async_client.get("/orders/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 3


@pytest.mark.asyncio(loop_scope='session')
async def test_get_order_by_id(async_client: AsyncClient):
    """
    Тест на получение заказа по ID.
    """
    expected_items = [
        {"product_id": 1, "quantity": 5},
        {"product_id": 2, "quantity": 3},
        {"product_id": 3, "quantity": 2}
    ]

    response = await async_client.get("/orders/1")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "in_progress"
    assert len(data["items"]) == 3

    for item, expected_item in zip(data["items"], expected_items):
        assert item["product_id"] == expected_item["product_id"]
        assert item["quantity"] == expected_item["quantity"]


@pytest.mark.asyncio(loop_scope='session')
async def test_update_product(async_client: AsyncClient):
    """
    Тест на обновление статуса заказа.
    """
    update_data = {"status": "delivered"}

    response = await async_client.patch("/orders/1/status", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == update_data["status"]
