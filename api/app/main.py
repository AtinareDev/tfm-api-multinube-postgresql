from fastapi import FastAPI

app = FastAPI(
    title="TFM API Multinube",
    description="API para gestionar datos en una arquitectura multinube con PostgreSQL.",
    version="0.1.0",
)


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
        "version": "0.1.0"
    }