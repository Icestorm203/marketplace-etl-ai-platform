# Marketplace ETL AI Platform

Backend-платформа для хранения, обработки и анализа данных маркетплейсов.

На текущем этапе проект представляет собой REST API на FastAPI с PostgreSQL, SQLAlchemy, Alembic, Docker и автоматическим тестированием через Pytest и GitHub Actions.

---

## Features

### Products

- Create product
- Get all products
- Get product by ID
- Update product
- Delete product

### Stocks

- Create stock
- Get all stocks
- Get stock by ID

### Sales

- Create sale
- Get all sales
- Get sale by ID

### Infrastructure

- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- Alembic migrations
- Docker Compose
- Pytest
- GitHub Actions CI

---

## Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL 17
- SQLAlchemy 2.0
- Alembic
- Pydantic
- Docker
- Docker Compose
- Pytest
- GitHub Actions

---

## Architecture

```text
app/
├── api/
│   ├── products.py
│   ├── stocks.py
│   └── sales.py
│
├── database/
│   └── database.py
│
├── models/
│   ├── product.py
│   ├── stock.py
│   └── sale.py
│
├── schemas/
│   ├── product.py
│   ├── stock.py
│   └── sale.py
│
├── services/
│   ├── product_service.py
│   ├── stock_service.py
│   └── sale_service.py
│
└── main.py

alembic/
tests/
.github/workflows/
```

---

## Database Schema

### Product

```text
Product
├── id
├── sku
├── name
├── purchase_price
├── sale_price
└── created_at
```

### Stock

```text
Stock
├── id
├── product_id
├── quantity
└── updated_at
```

### Sale

```text
Sale
├── id
├── product_id
├── quantity
├── sale_amount
└── sale_date
```

---

## Relationships

```text
Product
│
├── Stocks (1:N)
│
└── Sales (1:N)
```

---

# API Endpoints

## Products

### Create product

```http
POST /products
```

Request:

```json
{
  "sku": "SKU001",
  "name": "Mouse",
  "purchase_price": 500,
  "sale_price": 990
}
```

---

### Get all products

```http
GET /products
```

---

### Get product by id

```http
GET /products/{id}
```

---

### Update product

```http
PUT /products/{id}
```

Request:

```json
{
  "sku": "SKU001",
  "name": "Gaming Mouse",
  "purchase_price": 500,
  "sale_price": 1190
}
```

---

### Delete product

```http
DELETE /products/{id}
```

Response:

```json
{
  "message": "Product deleted"
}
```

---

## Stocks

### Create stock

```http
POST /stocks
```

Request:

```json
{
  "product_id": 1,
  "quantity": 100
}
```

---

### Get all stocks

```http
GET /stocks
```

---

### Get stock by id

```http
GET /stocks/{id}
```

---

## Sales

### Create sale

```http
POST /sales
```

Request:

```json
{
  "product_id": 1,
  "quantity": 3,
  "sale_amount": 2997
}
```

---

### Get all sales

```http
GET /sales
```

---

### Get sale by id

```http
GET /sales/{id}
```

---

## Error Handling

Example:

```http
GET /products/999
```

Response:

```json
{
  "detail": "Product not found"
}
```

Status code:

```http
404 Not Found
```

---

# Running Locally

## Clone repository

```bash
git clone <repository-url>
cd marketplace-etl-ai-platform
```

---

## Run application

```bash
docker compose up --build
```

Application:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```

OpenAPI:

```text
http://localhost:8000/redoc
```

---

# Migrations

Create migration:

```bash
docker compose run --rm app alembic revision --autogenerate -m "migration name"
```

Apply migrations:

```bash
docker compose run --rm app alembic upgrade head
```

Check current version:

```bash
docker compose run --rm app alembic current
```

---

# Testing

Test database:

```text
marketplace_test
```

Run tests:

```bash
docker compose run --rm app pytest -v
```

Current coverage includes:

- Product CRUD
- Stock creation and retrieval
- Sale creation and retrieval
- 404 validation
- Health endpoint

Current test suite:

```text
15 tests
```

---

# CI/CD

GitHub Actions automatically runs:

- Dependency installation
- Database migration check
- Pytest test suite

Workflow file:

```text
.github/workflows/tests.yml
```

---

# Roadmap

## MVP Backend ✅

- [x] FastAPI
- [x] PostgreSQL
- [x] SQLAlchemy
- [x] Alembic
- [x] Docker Compose
- [x] Product CRUD
- [x] Stocks API
- [x] Sales API
- [x] Pytest
- [x] GitHub Actions

## ETL Layer 🚧

- [ ] Wildberries API integration
- [ ] Marketplace data ingestion
- [ ] ETL pipelines
- [ ] Scheduled synchronization

## Analytics 🚧

- [ ] Revenue analytics
- [ ] Profit analytics
- [ ] Inventory analytics
- [ ] Product performance metrics

## AI Layer 🚧

- [ ] AI insights
- [ ] Demand forecasting
- [ ] Inventory recommendations

---

## Author

Mustafa Muratov

Backend Developer (Python / FastAPI / PostgreSQL)

Project created for learning backend development, ETL pipelines, marketplace integrations, testing, and CI/CD.