from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from app.core.config import settings


def get_database_url(cloud: str | None = None) -> str:
    selected_cloud = cloud or settings.active_cloud

    if selected_cloud == "aws":
        return settings.database_url_aws

    if selected_cloud == "azure":
        return settings.database_url_azure

    raise ValueError(f"Cloud no soportada: {selected_cloud}")


def create_database_engine(cloud: str | None = None) -> Engine:
    database_url = get_database_url(cloud)

    return create_engine(
        database_url,
        pool_pre_ping=True,
    )


def check_database_connection(cloud: str | None = None) -> dict:
    selected_cloud = cloud or settings.active_cloud

    try:
        engine = create_database_engine(selected_cloud)

        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            value = result.scalar_one()

        return {
            "cloud": selected_cloud,
            "status": "ok",
            "result": value,
        }

    except Exception as error:
        return {
            "cloud": selected_cloud,
            "status": "error",
            "error": str(error),
        }