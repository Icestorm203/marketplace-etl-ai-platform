import os

import pytest

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import Base
from app.database.database import get_db
from app.main import app

# Импорты регистрируют модели в Base.metadata
from app.models.product import Product
from app.models.sale import Sale
from app.models.stock import Stock


TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@postgres:5432/marketplace_test"
)

test_engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(autouse=True)
def clean_database():
    db = TestingSessionLocal()

    db.query(Sale).delete()
    db.query(Stock).delete()
    db.query(Product).delete()
    db.commit()
    db.close()

    yield

    db = TestingSessionLocal()

    db.query(Sale).delete()
    db.query(Stock).delete()
    db.query(Product).delete()
    db.commit()
    db.close()


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def product(client):
    response = client.post(
        "/products",
        json={
            "sku": "TEST-SKU-001",
            "name": "Test Product",
            "purchase_price": 500,
            "sale_price": 990
        }
    )

    assert response.status_code == 200
    return response.json()