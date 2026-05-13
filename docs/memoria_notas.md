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


## Fase 2 - CRUD de pedidos

Se ha implementado la gestión de pedidos mediante las entidades `orders` y `order_items`.

La API permite crear pedidos asociados a un cliente existente y a uno o varios productos existentes. Durante la creación del pedido, el sistema calcula el importe total a partir del precio de los productos y la cantidad solicitada.

También se ha añadido una validación básica de stock. Cuando se crea un pedido, el stock de los productos se reduce automáticamente. Si se elimina el pedido, el stock se restaura.

Los endpoints implementados permiten crear, listar, consultar, actualizar el estado y eliminar pedidos.



## Cierre de la Fase 2

Al finalizar la Fase 2, la API dispone de un modelo de datos relacional completo para gestionar clientes, productos y pedidos.

Se han implementado endpoints REST para las entidades principales:

- `customers`
- `products`
- `orders`
- `order_items`

La API trabaja contra la base de datos activa configurada inicialmente como AWS simulada. Las dos bases PostgreSQL locales, AWS y Azure simuladas, comparten el mismo esquema relacional.

La lógica de pedidos incluye validación de cliente, validación de productos, control básico de stock, cálculo automático del importe total y restauración de stock al eliminar pedidos.



## Fase 3 - Estado dinámico de cloud activa

Se ha sustituido el uso de una cloud activa fija por un mecanismo de estado dinámico almacenado en un archivo JSON local.

La API puede consultar la cloud activa mediante `/cloud/status`, y la capa de conexión a base de datos utiliza dicho estado para decidir si las operaciones deben ejecutarse contra la base PostgreSQL que simula AWS o contra la base PostgreSQL que simula Azure.

Inicialmente, la cloud activa se mantiene como `aws`.




## Fase 3 - Seguridad administrativa con API key

Se ha incorporado una protección básica mediante API key para endpoints administrativos de la API.

La clave se envía mediante la cabecera HTTP `X-API-Key`. En esta fase se han protegido los endpoints `/cloud/status` y `/db/init`.

Este mecanismo se utilizará también para proteger los futuros endpoints de conmutación entre clouds y sincronización de datos.