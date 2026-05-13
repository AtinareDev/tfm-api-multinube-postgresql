from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "TFM API Multinube"
    app_version: str = "0.3.0"

    active_cloud: str = "aws"

    admin_api_key: str = "tfm_admin_key"

    database_url_aws: str = (
        "postgresql+psycopg2://tfm_user:tfm_password@postgres_aws:5432/tfm_db"
    )
    database_url_azure: str = (
        "postgresql+psycopg2://tfm_user:tfm_password@postgres_azure:5432/tfm_db"
    )

    class Config:
        env_file = ".env"


settings = Settings()