# Marketplace ETL Platform

[![Tests](https://github.com/Icestorm203)](https://github.com/Icestorm203/marketplace-etl-ai-platform/actions/workflows/tests.yml)

Проект представляет собой backend-сервис на FastAPI для управления данными маркетплейса: товары, остатки, продажи и синхронизация с Shopify. Архитектура рассчитана на хранение данных в PostgreSQL, миграции через Alembic и дальнейшее расширение для аналитики и интеграций.

## Что умеет проект

- управление каталогом товаров
- учёт складских остатков
- учёт продаж
- OAuth-аутентификация Shopify
- синхронизация продуктов из Shopify через GraphQL API
- статистика по товарам Shopify
- проверки состояния API и базы данных
- поддержка Docker для локального запуска
- автоматическое тестирование (19 тестов)

## Технологии

- Python 3.12+
- FastAPI
- SQLAlchemy 2.0
- PostgreSQL
- Alembic
- Pydantic
- pytest
- Docker / Docker Compose
- Shopify Admin API
- GraphQL

## ETL-процесс

```text
Shopify
    ↓
OAuth Authentication
    ↓
Access Token
    ↓
GraphQL API
    ↓
Извлечение данных
    ↓
Pydantic Validation
    ↓
PostgreSQL
    ↓
REST API
```

## Структура проекта

```text
.
├── alembic/                  # миграции базы данных
├── app/
│   ├── api/                  # маршруты FastAPI
│   ├── database/             # конфигурация БД и сессии
│   ├── integrations/
│   │   └── shopify/          # интеграция с Shopify
│   ├── models/               # SQLAlchemy-модели
│   ├── schemas/              # Pydantic-схемы
│   ├── services/             # бизнес-логика
│   ├── main.py               # точка входа приложения
│   └── __init__.py
├── tests/                    # интеграционные/endpoint-тесты
├── .env.example              # пример переменных окружения
├── docker-compose.yml        # запуск PostgreSQL + приложения
├── Dockerfile                # образ приложения
├── requirements.txt          # зависимости
├── alembic.ini               # конфигурация Alembic
├── pytest.ini                # конфигурация pytest
└── README.md
```

## Основные сущности

### Product

Товар маркетплейса.

Поля:
- id
- sku
- name
- purchase_price
- sale_price
- created_at

### Stock

Остатки по товару.

Поля:
- id
- product_id
- quantity
- updated_at

### Sale

Продажа товара.

Поля:
- id
- product_id
- quantity
- sale_amount
- sale_date

### ShopifyProduct

Данные, импортированные из Shopify.

Поля:
- id
- title
- vendor
- status

## Переменные окружения

Скопируйте [.env.example](.env.example) в .env и заполните значения:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@postgres:5432/marketplace_db
POSTGRES_DB=marketplace_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

SHOPIFY_SHOP=
SHOPIFY_CLIENT_ID=
SHOPIFY_CLIENT_SECRET=
```

> Для локального запуска совместно с Docker переменные из .env автоматически подтягиваются в контейнер app.

## Запуск проекта

### Вариант 1: через Docker Compose

```bash
docker compose up --build
```

После запуска:
- API будет доступно на http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- PostgreSQL: localhost:5432

### Вариант 2: локально через Python

Для Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Для Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Если база ещё не создана, выполните миграции:

```bash
alembic upgrade head
```

## Проверка состояния сервисов

### Health-check

```bash
curl http://localhost:8000/health
```

Ожидаемый ответ:

```json
{"status": "ok"}
```

### Проверка соединения с БД

```bash
curl http://localhost:8000/db-check
```

## API

### Продукты

#### Создать товар

```http
POST /products
```

Тело запроса:

```json
{
  "sku": "SKU-001",
  "name": "Ноутбук",
  "purchase_price": 500.0,
  "sale_price": 899.0
}
```

#### Получить все товары

```http
GET /products
```

#### Получить товар по ID

```http
GET /products/{product_id}
```

#### Обновить товар

```http
PUT /products/{product_id}
```

#### Удалить товар

```http
DELETE /products/{product_id}
```

### Остатки

```http
POST /stocks
GET /stocks
GET /stocks/{stock_id}
```

Тело для создания остатка:

```json
{
  "product_id": 1,
  "quantity": 42
}
```

### Продажи

```http
POST /sales
GET /sales
GET /sales/{sale_id}
```

Тело для создания продажи:

```json
{
  "product_id": 1,
  "quantity": 2,
  "sale_amount": 1798.0
}
```

### Shopify

#### Импорт всех продуктов

```http
POST /shopify/products/sync
```

#### Получить список продуктов Shopify

```http
GET /shopify/products?limit=20&offset=0
```

#### Статистика по продуктам Shopify

```http
GET /shopify/products/stats
```

Пример ответа:

```json
{
  "total_products": 125,
  "active_products": 98,
  "draft_products": 17,
  "archived_products": 10
}
```

## Тестирование

Запуск всех тестов:

```bash
docker compose run --rm app pytest -v
```

или локально:

```bash
pytest -v
```

Текущий набор тестов: 19

Покрытие включает:

- Product API
- Stock API
- Sales API
- Shopify API
- Shopify статистику
- Shopify пагинацию
- Mock Shopify синхронизацию

```text
19 passed
```

## Миграции базы данных

Создание новой миграции:

```bash
alembic revision --autogenerate -m "description"
```

Применение миграций:

```bash
alembic upgrade head
```

## Примечания

- Проект предназначен для работы с каталогом товаров и потоками данных маркетплейса.
- Shopify интеграция использует OAuth-style аутентификацию и GraphQL API для синхронизации данных в PostgreSQL и требует корректной настройки переменных окружения `SHOPIFY_SHOP`, `SHOPIFY_CLIENT_ID` и `SHOPIFY_CLIENT_SECRET`.
- В текущем состоянии проект является базовой платформой для ETL и аналитики, которую можно расширять дополнительными источниками данных, агрегациями и AI-модулями.

## Полезные ссылки

- Swagger UI: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc
