# ADA-05-SPEC-DRIVEN — Customer Search

Sistema de búsqueda de clientes por nombre o correo electrónico desarrollado bajo la metodología **Spec-Driven Development**, arquitectura en capas desacoplada y modo de operación por línea de comandos (**CLI**).

---

## 1. Requisitos Previos

- **Python**: Versión 3.10 o superior (verificado con Python 3.11).
- **Pytest**: Framework para ejecución de pruebas unitarias y de integración.

---

## 2. Instalación y Preparación

1. Clonar o abrir el repositorio en el entorno de desarrollo.
2. (Opcional) Crear y activar un entorno virtual:
   ```bash
   python -m venv .venv
   # En Windows:
   .venv\Scripts\activate
   # En Linux / macOS:
   source .venv/bin/activate
   ```
3. Instalar la dependencia de pruebas si no se encuentra instalada:
   ```bash
   pip install pytest
   ```

---

## 3. Uso mediante CLI (Línea de Comandos)


### Búsqueda Directa con Argumentos

- **Búsqueda general por término (nombre o correo)**:
  ```bash
  python cli.py "Carlos"
  ```
- **Búsqueda delimitada a nombre (`--search-field name`)**:
  ```bash
  python cli.py "Carlos" --search-field name
  ```
- **Búsqueda delimitada a correo electrónico (`--search-field email`)**:
  ```bash
  python cli.py "empresa.com" --search-field email
  ```
- **Búsqueda específica por nombre**:
  ```bash
  python cli.py --name "Carlos Santana"
  ```
- **Búsqueda específica por correo electrónico**:
  ```bash
  python cli.py --email "soporte.ti@empresa.com"
  ```
- **Búsqueda con paginación, ordenamiento y campo delimitado**:
  ```bash
  python cli.py "example.com" --page 1 --limit 10 --order desc --search-field email
  ```

### Modo Interactivo

Al ejecutar sin argumentos, se inicia la consola interactiva:
```bash
python cli.py
```
Permite ingresar múltiples consultas de manera continua hasta escribir `salir` o `exit`.

---

## 4. Cómo Correr las Pruebas

Para ejecutar la suite de pruebas completa:

```bash
pytest -v
```

También es posible correr suites individuales:
- **Pruebas de la entidad de dominio**:
  ```bash
  pytest -v test_customer.py
  ```
- **Pruebas de la base de datos simulada**:
  ```bash
  pytest -v test_customers_data.py
  ```
- **Pruebas de búsqueda, criterios de aceptación (AC-01 a AC-06) y delimitación de campo (CR-01)**:
  ```bash
  pytest -v test_search_service.py
  ```
- **Pruebas de validación y control de errores (HTTP 400, 404, 500)**:
  ```bash
  pytest -v test_validation_and_errors.py
  ```
- **Pruebas de requerimientos no funcionales (NFR-01 rendimiento y NFR-02 rate limiting)**:
  ```bash
  pytest -v test_nfr.py
  ```

---

## 5. Uso Programático (API / Capas)

### Ejemplo 1: Búsqueda mediante la capa Handler

```python
from src.handler import CustomerSearchHandler

handler = CustomerSearchHandler()

# Búsqueda por nombre
response = handler.handle({"name": "Carlos"})
print(response)

# Búsqueda delimitando el campo a evaluar (CR-01)
response = handler.handle({"query": "Carlos", "search_field": "name"})
print(response)

# Búsqueda por correo electrónico
response = handler.handle({"email": "soporte.ti@empresa.com"})
print(response)

# Búsqueda con usuario autenticado (Rate Limiting NFR-02)
response = handler.handle({"query": "jose gomez"}, user_id="user_123")
print(response)
```

### Formato de Respuesta Exitosa (HTTP 200)

```json
{
  "status": 200,
  "message": "Búsqueda exitosa",
  "total": 1,
  "page": 1,
  "limit": 20,
  "order": "asc",
  "search_field": "all",
  "data": [
    {
      "id": "1",
      "name": "Carlos Santana",
      "email": "carlos.santana@example.com"
    }
  ]
}
```

---

## 6. Reglas de Negocio y Requerimientos

- **Normalización de Texto (FR-02)**: Insensible a mayúsculas/minúsculas y normalización automática de acentos y diéresis (e.g., `"jose gomez"` localiza `"José Gómez"`).
- **Coincidencias en Nombre y Correo (FR-01, FR-04, FR-06)**: Búsqueda por subcadena en nombre y coincidencia parcial en email (requiere al menos 3 caracteres consecutivos).
- **Delimitación de Campo de Búsqueda (CR-01, T-08)**: Soporte para parámetro opcional `search_field` con valores `'all'` (predeterminado), `'name'` y `'email'`. Permite delimitar las coincidencias exclusivamente al nombre o correo del cliente, excluyendo coincidencias del otro campo. Valores no permitidos generan un error de validación con código HTTP 400.
- **Orden de Relevancia Estricto y Configurable (AC-06, T-07)**:
  1. Coincidencia exacta en nombre
  2. Coincidencia exacta en correo
  3. Coincidencia por prefijo en nombre
  4. Coincidencia por prefijo en correo
  5. Coincidencia por subcadena en nombre
  6. Coincidencia por subcadena en correo
  *Desempate*: Orden alfabético configurable por nombre mediante el parámetro `order` (`"asc"` para A-Z por defecto, o `"desc"` para Z-A). Valores no válidos son rechazados con código HTTP 400.
- **Protección de Datos Sensibles (FR-05, AC-05)**: El DTO de salida únicamente entrega campos básicos autorizados (`id`, `name`, `email`). Atributos sensibles nunca son expuestos.
- **Paginación**: Segmentación con límite predeterminado de 20 elementos por página.
- **Rendimiento Bajo Carga (NFR-01)**: Latencia p95 verificada $\le$ 300 ms bajo 50 peticiones concurrentes.
- **Rate Limiting (NFR-02)**: Máximo 30 peticiones por minuto por usuario autenticado. Al excederse, se rechaza con código HTTP 429 (`Too Many Requests`).
- **Manejo de Errores**:
  - **400 Bad Request**: Términos vacíos, de sólo espacios, con longitud inferior a 3 caracteres o parámetros inválidos (`order`, `search_field`).
  - **404 Not Found**: Sin coincidencias, mostrando exactamente `"No se encontraron clientes para '{término}'"`.
  - **429 Too Many Requests**: Superado el límite de 30 peticiones por minuto por usuario.
  - **500 Internal Server Error**: Captura de fallos de persistencia o errores internos no controlados.

---

## 7. Arquitectura y Componentes

El proyecto sigue una arquitectura en capas:

- **CLI (`cli.py`)**: Interfaz de consola interactiva y por comandos con soporte para flags `--page`, `--limit`, `--order` y `--search-field`.
- **Handler (`handler.py`)**: Punto de entrada de solicitudes HTTP/payloads; gestiona el rate limiting por usuario (NFR-02) e inyecta datos al servicio.
- **Service (`search_services.py`)**: Coordina las reglas de negocio, normalización, filtrado por campo (`search_field`), ordenamiento por relevancia y empaquetado de DTOs.
- **Domain (`customer.py`)**: Entidad de negocio `Customer` con atributos esenciales (`id`, `nombre`/`name`, `email`).
- **Repository (`customer_repository.py`)**: Acceso desacoplado a la persistencia simulada de clientes en `customers.json`.
- **Exceptions (`exceptions.py`)**: Jerarquía formal de excepciones de dominio (`CustomerSearchException`, `EmptyQueryError`, `ValidationError`, `CustomerNotFoundError`, `DatabaseError`, `RateLimitExceededError`).
- **Data (`customers.json`)**: Base de datos simulada en memoria con 52 registros únicos.
