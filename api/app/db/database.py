from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.db.base import Base
from app import models


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


def create_session_factory(cloud: str | None = None):
    engine = create_database_engine(cloud)

    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )


def get_db():
    SessionLocal = create_session_factory()

    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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


def init_database(cloud: str | None = None) -> dict:
    selected_cloud = cloud or settings.active_cloud

    try:
        engine = create_database_engine(selected_cloud)
        Base.metadata.create_all(bind=engine)

        return {
            "cloud": selected_cloud,
            "status": "ok",
            "message": "Tablas creadas correctamente",
        }

    except Exception as error:
        return {
            "cloud": selected_cloud,
            "status": "error",
            "error": str(error),
        }


def init_all_databases() -> dict:
    return {
        "databases": [
            init_database("aws"),
            init_database("azure"),
        ]
    }


def list_database_tables(cloud: str | None = None) -> dict:
    selected_cloud = cloud or settings.active_cloud

    try:
        engine = create_database_engine(selected_cloud)
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        return {
            "cloud": selected_cloud,
            "status": "ok",
            "tables": tables,
        }

    except Exception as error:
        return {
            "cloud": selected_cloud,
            "status": "error",
            "error": str(error),
        }


def list_all_database_tables() -> dict:
    return {
        "databases": [
            list_database_tables("aws"),
            list_database_tables("azure"),
        ]
    }