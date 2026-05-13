from fastapi import Depends, FastAPI, HTTPException, status

from app.api.routes.customers import router as customers_router
from app.api.routes.orders import router as orders_router
from app.api.routes.products import router as products_router
from app.core.cloud_state import (
    get_active_cloud,
    get_available_clouds,
    write_active_cloud,
)
from app.core.config import settings
from app.core.security import verify_api_key
from app.db.database import (
    check_database_connection,
    init_all_databases,
    list_all_database_tables,
)
from app.schemas.cloud import CloudSwitchRequest, CloudSwitchResponse

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
def cloud_status(_: None = Depends(verify_api_key)):
    return {
        "active_cloud": get_active_cloud(),
        "available_clouds": get_available_clouds(),
    }


@app.post(
    "/cloud/switch",
    response_model=CloudSwitchResponse,
)
def switch_cloud(
    switch_request: CloudSwitchRequest,
    _: None = Depends(verify_api_key),
):
    target_cloud = switch_request.target_cloud.lower()
    available_clouds = get_available_clouds()

    if target_cloud not in available_clouds:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cloud no soportada: {target_cloud}. Valores permitidos: {available_clouds}",
        )

    previous_cloud = get_active_cloud()

    if target_cloud == previous_cloud:
        return {
            "previous_cloud": previous_cloud,
            "active_cloud": previous_cloud,
            "status": "ok",
            "message": f"La cloud activa ya era {previous_cloud}.",
        }

    target_health = check_database_connection(target_cloud)

    if target_health.get("status") != "ok":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"No se puede cambiar a {target_cloud}. La base de datos destino no está disponible.",
        )

    write_active_cloud(target_cloud)

    return {
        "previous_cloud": previous_cloud,
        "active_cloud": target_cloud,
        "status": "ok",
        "message": f"Cloud activa cambiada de {previous_cloud} a {target_cloud}.",
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
def database_init(_: None = Depends(verify_api_key)):
    return init_all_databases()


@app.get("/db/tables")
def database_tables():
    return list_all_database_tables()