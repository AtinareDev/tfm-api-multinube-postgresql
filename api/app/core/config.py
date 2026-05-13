from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "TFM API Multinube"
    app_version: str = "0.2.0"

    active_cloud: str = "aws"

    database_url_aws: str = (
        "postgresql+psycopg2://tfm_user:tfm_password@postgres_aws:5432/tfm_db"
    )
    database_url_azure: str = (
        "postgresql+psycopg2://tfm_user:tfm_password@postgres_azure:5432/tfm_db"
    )

    class Config:
        env_file = ".env"


settings = Settings()