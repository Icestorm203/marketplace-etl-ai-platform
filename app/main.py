from fastapi import FastAPI

from sqlalchemy import text

from app.database.database import engine
from app.api.products import router as products_router
from app.api.stocks import router as stocks_router
from app.api.sales import router as sales_router
from app.api.shopify import router as shopify_router

app = FastAPI(
    title="Marketplace ETL & AI Analytics Platform"
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/db-check")
async def db_check():

    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT 1")
        )

        return {
            "database": "connected",
            "result": result.scalar()
        }


app.include_router(products_router)
app.include_router(stocks_router)
app.include_router(sales_router)
app.include_router(shopify_router)
