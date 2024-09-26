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
* Документация:
  - Используется встроенная документация FastAPI (Swagger/OpenAPI).
### Бизнес-логика:
* При создании заказа проверятся наличие достаточного количества товара на складе.
* Обновлятся количество товара на складе при создании заказа (уменьшение доступного количества).
* В случае недостаточного количества товара – возвращается ошибка с соответствующим сообщением.
### Для развертывания приложения необходимо:
1. Склонировать проект к себе git clone github.com:ваш-аккаунт-на-гитхабе/Test-warehouse.git
2. В склонированном репозитории создайте и активируйте виртуальное окружение(Рекомендованная версия Python - 3.12)
3. Установите зависимости ```pip install -r requirements.txt```
4. В корне проекта создайте файл .env и заполните его. Необходимые переменные можно найти в app/core/config.py. Обращаю внимание, что названия переменных должны совпадать, но в .env названия необходимо писать большими буквами.
5. Запустите API командой ```uvicorn app.main:app --reload```. По ссылке http://127.0.0.1:8000/docs будет доступна документация Swagger. По ссылке http://127.0.0.1:8000/redoc будет доступна документация ReDoc.
### Подключение миграций:
1. Запустите postgres с заданными в .env параметрами
2. Находясь в корне проекта инициализируйте Alembic командой:
```alembic init -t async migrations```
3. Перейдите в создавшуюся папку migrations и откройте файл env.py
5. Дополните импорты 
```
from app.core.db import DATABASE_URL, Base
from app.models import Product # noqa
```
5. После строки *config = context.config* допишите:
```config.set_main_option('sqlalchemy.url', DATABASE_URL)```
6. Спуститесь ниже к строке *target_metadata = None* и замените ее на:
```target_metadata = Base.metadata```
7. Запустите автогенерацию миграций:
```alembic revision --autogenerate -m "First migration"```
8. Примените миграции:
```alembic upgrade head ```
### Для развертывания приложения с помощью Docker Compose необходимо:
1. Склонировать проект к себе git clone github.com:ваш-аккаунт-на-гитхабе/Test-warehouse.git
2. В корне проекта создайте файл .env и заполните переменными:
```
APP_TITLE=API для управления складом  #Название, которое будет отображаться в Swagger и ReDoc
DB_USER=<впишите имя пользователя для postgres>
DB_PASSWORD=<впишите пароль для postgres>
DB_NAME=<впишите имя базы банных postgres>
DB_PORT=5432
DB_HOST=postgres
```
3. В терминале из директории с проектом запустить docker compose командой:
```docker compose up -d --build```
4. После запуска контейнеров инициализируйте Alembic с помощью асинхронного шаблона:
```docker compose exec web alembic init -t async migrations```
5. Локально выполните пункты с 3 по 6 включительно "Подключение миграций"
6. В терминале из директории с проектом создайте первый файл миграции:
```docker compose exec web alembic revision --autogenerate -m "init"```
7. Примените миграции ```docker compose exec web alembic upgrade head```
