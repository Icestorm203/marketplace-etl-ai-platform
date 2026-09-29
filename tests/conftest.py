import os

import psycopg2
import pytest

from fastapi.testclient import TestClient

from psycopg2 import sql

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker

from app.database.database import Base
from app.database.database import get_db
from app.main import app

# Регистрируем модели в Base.metadata
from app.models.product import Product
from app.models.sale import Sale
from app.models.shopify_product import ShopifyProduct
from app.models.stock import Stock


TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    (
        "postgresql+psycopg2://"
        "postgres:postgres@postgres:5432/marketplace_test"
    ),
)

test_url = make_url(TEST_DATABASE_URL)
test_database_name = test_url.database

test_engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


def get_admin_connection():
    connection = psycopg2.connect(
        dbname="postgres",
        user=test_url.username,
        password=test_url.password,
        host=test_url.host,
        port=test_url.port,
    )

    connection.autocommit = True

    return connection


def create_test_database():
    connection = get_admin_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT 1
                FROM pg_database
                WHERE datname = %s
                """,
                (test_database_name,),
            )

            database_exists = cursor.fetchone()

            if not database_exists:
                cursor.execute(
                    sql.SQL(
                        "CREATE DATABASE {}"
                    ).format(
                        sql.Identifier(test_database_name)
                    )
                )
    finally:
        connection.close()


def drop_test_database():
    connection = get_admin_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                WHERE datname = %s
                  AND pid <> pg_backend_pid()
                """,
                (test_database_name,),
            )

            cursor.execute(
                sql.SQL(
                    "DROP DATABASE IF EXISTS {}"
                ).format(
                    sql.Identifier(test_database_name)
                )
            )
    finally:
        connection.close()


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    create_test_database()

    Base.metadata.create_all(
        bind=test_engine
    )

    yield

    Base.metadata.drop_all(
        bind=test_engine
    )

    test_engine.dispose()

    drop_test_database()

    app.dependency_overrides.clear()


def clear_tables():
    db = TestingSessionLocal()

    try:
        db.query(Sale).delete()
        db.query(Stock).delete()
        db.query(ShopifyProduct).delete()
        db.query(Product).delete()

        db.commit()
    finally:
        db.close()


@pytest.fixture(autouse=True)
def clean_database():
    clear_tables()

    yield

    clear_tables()


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
            "sale_price": 990,
        },
    )

    assert response.status_code == 200

    return response.json()