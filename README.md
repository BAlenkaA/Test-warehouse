# Test-warehouse
## Test-warehouse - это REST API с использованием FastAPI для управления процессами на складе. API позволяет управлять товарами, складскими запасами и заказами. ##
### Стек:
* FastApi
* Postgres (asyncpg)
* SQLAlchemy (2 версия)
* Миграции БД с помощью Alembic
### Реализация REST API:
* Эндпоинты для товаров:
  - Создание товара (POST /products)
  - Получение списка товаров (GET /products)
  - Получение информации о товаре по id (GET /products/{id})
  - Обновление информации о товаре (PUT /products/{id})
  - Удаление товара (DELETE /products/{id})
* Эндпоинты для заказов:
  - Создание заказа (POST /orders)
  - Получение списка заказов (GET /orders)
  - Получение информации о заказе по id (GET /orders/{id})
  - Обновление статуса заказа (PATCH /orders/{id}/status)
### Бизнес-логика:
* При создании заказа проверятся наличие достаточного количества товара на складе.
* Обновлятся количество товара на складе при создании заказа (уменьшение доступного количества).
* В случае недостаточного количества товара – возвращается ошибка с соответствующим сообщением.