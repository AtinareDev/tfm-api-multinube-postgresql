# Notas para la memoria del TFM

## Tema

Diseño e implementación de una API multinube con PostgreSQL sobre AWS y Azure.

## Alcance inicial

El desarrollo comenzará en local usando Docker para simular dos proveedores cloud:

- PostgreSQL AWS simulado
- PostgreSQL Azure simulado

Posteriormente, si es viable, se sustituirán las bases de datos locales por servicios PostgreSQL reales en AWS y Azure.

## Decisiones técnicas iniciales

- Backend: FastAPI
- Base de datos: PostgreSQL
- ORM: SQLAlchemy
- Aplicación cliente: Streamlit
- Contenedores: Docker y Docker Compose
- Seguridad: API key simple para endpoints administrativos
- Conmutación: manual desde la aplicación Streamlit
- Sincronización: antes de cambiar de cloud activa


## Fase 1 - API inicial con FastAPI

Se ha creado una primera versión de la API usando FastAPI. La API se ejecuta en Docker y expone dos endpoints iniciales:

- `/`: endpoint raíz para comprobar que la API responde.
- `/health`: endpoint de salud del servicio.

La documentación interactiva se genera automáticamente mediante Swagger/OpenAPI en `/docs`.

## Fase 1 - Aplicación cliente inicial con Streamlit

Se ha creado una aplicación cliente sencilla con Streamlit. Esta aplicación consume el endpoint `/health` de la API FastAPI para comprobar el estado del backend.

La aplicación se ejecuta en Docker y queda expuesta en el puerto local `8501`.