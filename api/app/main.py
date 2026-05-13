from fastapi import FastAPI

from app.api.routes.customers import router as customers_router
from app.api.routes.orders import router as orders_router
from app.api.routes.products import router as products_router
from app.core.cloud_state import get_active_cloud, get_available_clouds
from app.core.config import settings
from app.db.database import (
    check_database_connection,
    init_all_databases,
    list_all_database_tables,
)

app = FastAPI(
    title=settings.app_name,
    description="API para gestionar datos en una arquitectura multinube con PostgreSQL.",
    version=settings.app_version,
)

app.include_router(customers_router)
app.include_router(products_router)
app.include_router(orders_router)


@app.get("/")
def root():
    return {
        "message": "TFM API Multinube funcionando correctamente"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "api",
        "version": settings.app_version,
    }


@app.get("/cloud/status")
def cloud_status():
    return {
        "active_cloud": get_active_cloud(),
        "available_clouds": get_available_clouds(),
    }


@app.get("/db/health")
def database_health():
    return check_database_connection()


@app.get("/db/health/all")
def database_health_all():
    return {
        "databases": [
            check_database_connection("aws"),
            check_database_connection("azure"),
        ]
    }


@app.post("/db/init")
def database_init():
    return init_all_databases()


@app.get("/db/tables")
def database_tables():
    return list_all_database_tables()