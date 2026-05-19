# E-Commerce Microservicios

Este repositorio contiene una plataforma de comercio electrónico basada en microservicios con FastAPI, SQLAlchemy y despliegue en Kubernetes.

## Arquitectura

El proyecto está organizado en cinco microservicios independientes:

- `auth-service`: gestión de usuarios y autenticación JWT.
- `product-service`: catálogo de productos y CRUD básico.
- `inventory-service`: inventario y reserva de stock.
- `order-service`: creación de órdenes con validación de producto y reserva de inventario.
- `user-service`: gestión de datos de usuarios.

Cada servicio usa FastAPI, crea sus modelos SQLAlchemy y expone su propia API.

## Tecnologías principales

- Python 3.9 / 3.11
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn
- PostgreSQL (en Kubernetes)
- HTTPX (comunicación entre servicios)
- Kubernetes (manifiestos en `k8s/`)

## Servicios y endpoints

### auth-service

- `GET /auth/health` - estado del servicio.
- `POST /auth/register` - registra un usuario.
- `POST /auth/login` - genera un token JWT.

### product-service

- `GET /products/` - lista todos los productos.
- `POST /products/` - crea un producto.

### inventory-service

- `GET /inventory/{product_id}` - consulta stock por producto.
- `POST /inventory/reserve` - reserva stock para un producto.

### order-service

- `GET /orders/health` - estado del servicio.
- `POST /orders/` - crea una orden.

El servicio de órdenes llama a:
- `PRODUCT_SERVICE_URL` para validar la existencia del producto.
- `INVENTORY_SERVICE_URL` para reservar stock.

### user-service

- `POST /users/` - crea un usuario.
- `GET /users/{user_id}` - obtiene un usuario por id.

## Base de datos

Todos los servicios usan SQLAlchemy con un `DATABASE_URL` proporcionado por variables de entorno.

El proyecto incluye configuración de Kubernetes para PostgreSQL en `k8s/database/`.

## Despliegue en Kubernetes

Manifiestos principales:

- `k8s/namespace.yaml` - namespace `ecommerce`.
- `k8s/configmap.yaml` - variables de entorno comunes.
- `k8s/auth-service/services.yaml`
- `k8s/product-service/service.yaml`
- `k8s/inventory-service/service.yaml`
- `k8s/order-service/service.yaml`
- `k8s/user-service/service.yaml`
- `k8s/ingress/ingress.yaml` - enrutamiento HTTP a los servicios.

> Nota: revisa el mapeo de puertos en el `Ingress` y en los servicios para que coincidan con los puertos expuestos por cada microservicio.

## Variables de entorno clave

Configuradas en `k8s/configmap.yaml`:

- `PRODUCT_SERVICE_URL` - URL del servicio de productos.
- `INVENTORY_SERVICE_URL` - URL del servicio de inventario.
- `JWT_SECRET` - secreto JWT.
- `DATABASE_URL` - conexión a PostgreSQL.
- `APP_ENV`
- `LOG_LEVEL`

## Ejecución local

Cada servicio tiene su propio `dockerfile` en `services/<servicio>/dockerfile`.

Puertos por servicio:

- `auth-service`: 8003
- `product-service`: 8000
- `inventory-service`: 8001
- `order-service`: 8002
- `user-service`: 8004

## Ejemplos de uso

Registrar usuario:

```bash
curl -X POST http://localhost:8003/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"username":"user1","password":"pass123"}'
```

Crear producto:

```bash
curl -X POST http://localhost:8000/products/ \
  -H 'Content-Type: application/json' \
  -d '{"name":"Producto A","price":99.99}'
```

Reservar inventario:

```bash
curl -X POST http://localhost:8001/inventory/reserve \
  -H 'Content-Type: application/json' \
  -d '{"product_id":1,"quantity":2}'
```

Crear orden:

```bash
curl -X POST http://localhost:8002/orders/ \
  -H 'Content-Type: application/json' \
  -d '{"product_id":1,"quantity":2}'
```

## Observaciones

- `order-service` realiza validación remota de producto e inventario antes de crear la orden.
- `auth-service` guarda usuarios y valida credenciales con contraseña hasheada.
- El servicio `user-service` ofrece datos de usuario adicionales separados de `auth-service`.

## Siguientes pasos sugeridos

- añadir pruebas unitarias / de integración.
- implementar autenticación y autorización en `order-service`.
- añadir manejo de errores y logging más detallado.
- revisar la configuración de ingress y los puertos para evitar conflictos.
