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



## Fase 2 - Conexión inicial con PostgreSQL

Se ha añadido la conexión de la API FastAPI con las dos bases de datos PostgreSQL locales que simulan AWS y Azure.

La API incorpora endpoints para consultar la cloud activa y comprobar la conectividad con la base de datos activa o con ambas bases de datos:

- `/cloud/status`
- `/db/health`
- `/db/health/all`

Inicialmente, la cloud activa configurada es AWS.



## Fase 2 - Modelo de datos relacional

Se ha definido el modelo de datos principal del sistema mediante SQLAlchemy.

El dominio elegido para el TFM se basa en una gestión sencilla de negocio con las siguientes entidades:

- `customers`: clientes.
- `products`: productos.
- `orders`: pedidos.
- `order_items`: líneas de pedido.

El modelo incluye relaciones entre clientes y pedidos, así como entre pedidos, líneas de pedido y productos.

Las tablas se han creado en las dos bases PostgreSQL locales que simulan AWS y Azure.

## Fase 2 - Esquemas de validación con Pydantic

Se han creado los esquemas Pydantic para las entidades `customers` y `products`.

Estos esquemas permiten validar los datos de entrada y estructurar las respuestas de la API. Se han definido esquemas separados para creación, actualización y lectura de datos:

- `CustomerCreate`
- `CustomerUpdate`
- `CustomerRead`
- `ProductCreate`
- `ProductUpdate`
- `ProductRead`

Esta separación facilita construir endpoints REST más claros y seguros.



## Fase 2 - CRUD de clientes

Se ha implementado el primer conjunto de endpoints CRUD de la API para la entidad `customers`.

Los endpoints permiten:

- Crear clientes.
- Listar clientes.
- Consultar un cliente por identificador.
- Actualizar los datos de un cliente.
- Eliminar clientes.

La API utiliza SQLAlchemy para acceder a PostgreSQL y Pydantic para validar los datos de entrada y salida.


## Fase 2 - CRUD de productos

Se ha implementado el conjunto de endpoints CRUD para la entidad `products`.

Los endpoints permiten:

- Crear productos.
- Listar productos.
- Consultar un producto por identificador.
- Actualizar los datos de un producto.
- Eliminar productos.

La entidad `products` incluye información básica como nombre, descripción, precio y stock disponible.