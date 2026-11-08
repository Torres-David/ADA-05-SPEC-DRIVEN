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
  python src/cli.py "Carlos"
  ```
- **Búsqueda específica con ámbito de campo (`--search-field`)**:
  ```bash
  # Limitar búsqueda exclusivamente a nombres:
  python src/cli.py "Carlos" --search-field name

  # Limitar búsqueda exclusivamente a correos:
  python src/cli.py "emp" --search-field email

  # Búsqueda en ambos campos (por defecto):
  python src/cli.py "Carlos" --search-field all
  ```
- **Búsqueda específica por nombre**:
  ```bash
  python src/cli.py --name "Carlos Santana"
  ```
- **Búsqueda específica por correo electrónico**:
  ```bash
  python src/cli.py --email "soporte.ti@empresa.com"
  ```
- **Búsqueda con paginación, ordenamiento y ámbito de campo**:
  ```bash
  python src/cli.py "example.com" --page 1 --limit 10 --order desc --search-field email
  ```

### Modo Interactivo

Al ejecutar sin argumentos, se inicia la consola interactiva:
```bash
python src/cli.py
```
Permite ingresar múltiples consultas de manera continua hasta escribir `salir` o `exit`.

---

## 4. Cómo Correr las Pruebas

Para ejecutar la suite de pruebas completa (77 pruebas automáticas):

```bash
pytest -v
```

También es posible correr suites individuales:
- **Pruebas de la entidad de dominio**:
  ```bash
  pytest -v test/test_customer.py
  ```
- **Pruebas de la base de datos simulada**:
  ```bash
  pytest -v test/test_customers_data.py
  ```
- **Pruebas de búsqueda, ordenamiento y ámbito de campo (AC-01..AC-06, T-07, CR-01)**:
  ```bash
  pytest -v test/test_search_service.py
  ```
- **Pruebas de validación y control de errores (HTTP 400, 404, 500)**:
  ```bash
  pytest -v test/test_validation_and_errors.py
  ```
- **Pruebas de requerimientos no funcionales (NFR-01 rendimiento y NFR-02 rate limiting)**:
  ```bash
  pytest -v test/test_nfr.py
  ```
- **Verificación determinista del repositorio**:
  ```bash
  python scripts/verify_repo.py
  ```

---

## 5. Uso Programático (API / Capas)

### Ejemplo 1: Búsqueda mediante la capa Handler

```python
from src.handler import CustomerSearchHandler

handler = CustomerSearchHandler()

# Búsqueda general en todos los campos (por defecto)
response = handler.handle({"query": "Carlos"})
print(response)

# Búsqueda con ámbito de campo acotado a nombres
response = handler.handle({"query": "Carlos"}, search_field="name")
print(response)

# Búsqueda con ámbito de campo acotado a correos
response = handler.handle({"query": "emp"}, search_field="email")
print(response)

# Búsqueda mediante diccionario de solicitud con ordenamiento y ámbito
response = handler.handle(
    {"query": "Carlos", "order": "desc", "search_field": "name"}
)
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
  "search_field": "name",
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
- **Ámbito de Búsqueda Configurable (CR-01)**:
  - `search_field='name'`: Coincide únicamente contra nombres de clientes; coincidencias exclusivas por correo son omitidas.
  - `search_field='email'`: Coincide únicamente contra correos electrónicos de clientes; coincidencias exclusivas por nombre son omitidas.
  - `search_field='all'` (o ausente/None): Evalúa coincidencias en ambos campos, manteniendo compatibilidad hacia atrás.
  - Valores no permitidos generan `ValidationError` con código HTTP 400 (`Bad Request`).
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
  - **400 Bad Request**: Términos vacíos, de sólo espacios, con longitud inferior a 3 caracteres, parámetro `order` inválido o parámetro `search_field` no permitido.
  - **404 Not Found**: Sin coincidencias, mostrando exactamente `"No se encontraron clientes para '{término}'"`.
  - **429 Too Many Requests**: Superado el límite de 30 peticiones por minuto por usuario.
  - **500 Internal Server Error**: Captura de fallos de persistencia o errores internos no controlados.

---

## 7. Arquitectura y Componentes

El proyecto sigue una arquitectura en capas:

- **CLI (`src/cli.py`)**: Interfaz de consola interactiva y por comandos.
- **Handler (`src/handler.py`)**: Punto de entrada de solicitudes HTTP/payloads; gestiona el rate limiting por usuario (NFR-02) e inyecta datos al servicio.
- **Service (`src/search_services.py`)**: Coordina las reglas de negocio, normalización, filtrado por ámbito (`search_field`), ordenamiento por relevancia y empaquetado de DTOs.
- **Domain (`src/customer.py`)**: Entidad de negocio `Customer` con atributos esenciales (`id`, `nombre`/`name`, `email`).
- **Repository (`src/customer_repository.py`)**: Acceso desacoplado a la persistencia simulada de clientes en `src/customers.json`.
- **Exceptions (`src/exceptions.py`)**: Jerarquía formal de excepciones de dominio (`CustomerSearchException`, `EmptyQueryError`, `ValidationError`, `CustomerNotFoundError`, `DatabaseError`, `RateLimitExceededError`).
- **Data (`src/customers.json`)**: Base de datos simulada en memoria con 52 registros únicos.
