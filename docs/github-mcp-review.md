# GitHub MCP Engineering Review — ADA-06

## 1. Repository
Owner / Repo: `Torres-David/ADA-05-SPEC-DRIVEN`  
Visibility: Public  
Branch / reference analyzed: `main` (commit base [`99eb27225936b2989636f656aa48a418d409b944`](https://github.com/Torres-David/ADA-05-SPEC-DRIVEN/commit/99eb27225936b2989636f656aa48a418d409b944)), `Cambio-ADA-06` (PR #2, commit [`24a3d32c3e8cfb9f0221f85b4f3a8609a3ad2da5`](https://github.com/Torres-David/ADA-05-SPEC-DRIVEN/commit/24a3d32c3e8cfb9f0221f85b4f3a8609a3ad2da5)), [Issue #1](https://github.com/Torres-David/ADA-05-SPEC-DRIVEN/issues/1).  

---

## 2. MCP Connection
Server: `github-readonly`  
Mode: READ-ONLY  
Toolsets:
- `repos`: `get_file_contents`, `search_code`, `list_commits`, `get_commit`, `list_branches`, `search_repositories`
- `issues`: `list_issues`, `issue_read`, `search_issues`, `list_issue_fields`, `list_issue_types`
- `pull_requests`: `list_pull_requests`, `pull_request_read`, `search_pull_requests`

---

## 3. Repository Understanding
Purpose:
- Implementación de un motor de búsqueda de clientes (*Customer Search*) siguiendo rigurosamente la metodología **Spec-Driven Development (SDD)** en Python.
- Normalización lingüística avanzada: insensible a mayúsculas/minúsculas y remoción de acentos/diéresis (Unicode NFD).
- Algoritmo de relevancia estricto en 6 niveles jerárquicos (coincidencia exacta > prefijo > subcadena) con desempate alfabético por nombre.
- Protección estricta de datos confidenciales (`password_hash`, `tax_id`) mediante DTOs seguros.
- Cumplimiento de requerimientos no funcionales: latencia p95 $\le$ 300 ms bajo 50 peticiones concurrentes ([`NFR-01`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/REQUIREMENTS.md#L16)) y rate limiting de 30 req/min por usuario con código HTTP 429 ([`NFR-02`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/REQUIREMENTS.md#L17)).

Architecture summary:
- **Arquitectura en Capas (Layered / Clean Architecture):**
  - **Presentación / Adaptadores:** [`src/cli.py`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/cli.py) (CLI directo e interactivo) y [`src/handler.py`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/handler.py) (`CustomerSearchHandler` como fachada de entrada y `RateLimiter` en memoria).
  - **Servicios / Lógica de Negocio:** [`src/search_services.py`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/search_services.py) (`CustomerSearchService`, normalización de texto y ordenamiento por relevancia y desempate).
  - **Dominio:** [`src/customer.py`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/customer.py) (entidad `Customer` con sanitización en `to_dict`) y [`src/exceptions.py`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/exceptions.py) (jerarquía de excepciones asociadas a códigos HTTP 400, 404, 429, 500).
  - **Persistencia:** [`src/customer_repository.py`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/customer_repository.py) (`CustomerRepository` sobre [`src/customers.json`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/customers.json)).

Important files:
- Fuentes: [`src/cli.py`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/cli.py), [`src/handler.py`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/handler.py), [`src/search_services.py`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/search_services.py), [`src/customer.py`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/customer.py), [`src/customer_repository.py`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/customer_repository.py), [`src/exceptions.py`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/exceptions.py).
- Especificación y gobierno: [`REQUIREMENTS.md`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/REQUIREMENTS.md), [`SPEC.md`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/SPEC.md), [`ARCHITECTURE.md`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/ARCHITECTURE.md), [`TASKS.md`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/TASKS.md), [`AGENTS.md`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/AGENTS.md), [`docs/Trazabilidad.md`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/docs/Trazabilidad.md).

Tests:
- 47 pruebas automáticas distribuidas en [`test/`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/test/): `test_customer.py` (9), `test_customers_data.py` (5), `test_nfr.py` (3), `test_search_service.py` (21) y `test_validation_and_errors.py` (9). Configuración en [`pytest.ini`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/pytest.ini). Estado: **100% pasando en 0.10s**.

---

## 4. Issue Analysis
Issue:
- [Issue #1](https://github.com/Torres-David/ADA-05-SPEC-DRIVEN/issues/1): `FEATURE: Soporte de filtro por orden ascendente o descendiente` (Estado: `OPEN`, Autor: `Torres-David`, Creación: 2026-10-01T23:50:38Z).

Facts from Issue:
- Título textual: `"FEATURE: Soporte de filtro por orden ascendente o descendiente"`.
- Cuerpo (`body`): Vacío (`null` / sin descripción).
- Metadatos: 0 labels, 0 assignees, 0 comentarios, sin milestone.
- Ausencia de criterios de aceptación explícitos o plantilla en GitHub.

Ambiguities:
- Término impreciso ("filtro" vs "ordenamiento"): se requería ordenamiento (*sort order*), no filtrado condicional.
- Parámetro y valores aceptados: nombre (`order`, `sort`), valores (`asc`/`desc`), insensibilidad a mayúsculas y espacios.
- Regla de negocio ante el orden inverso: ¿afecta a la jerarquía de relevancia completa o solo al desempate alfabético por nombre?
- Manejo de entradas inválidas: ¿excepción de validación (HTTP 400) o fallback a `"asc"`?
- Superficie de exposición: banderas CLI (`--order`), payload JSON y metadato en la respuesta DTO.

Related requirements/spec:
- [`SPEC.md`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/SPEC.md) (Sección *Search Rules*, líneas 28-29 y Criterio [`AC-06`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/SPEC.md#L52)).
- [`TASKS.md`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/TASKS.md) (Tarea formal [`T-07 Configurable sort order`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/TASKS.md#L32)).
- [`docs/Trazabilidad.md`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/docs/Trazabilidad.md) (Requerimiento derivado formalizado [`FR-Sort`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/docs/Trazabilidad.md#L12)).

Related code:
- [`src/search_services.py`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/search_services.py) ([`search_customers()`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/search_services.py#L107), [`search()`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/search_services.py#L201)).
- [`src/handler.py`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/handler.py) ([`CustomerSearchHandler.handle()`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/handler.py#L65)).
- [`src/cli.py`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/cli.py) (`argparse` y [`format_search_results()`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/cli.py#L13)).
- [`src/exceptions.py`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/exceptions.py) ([`ValidationError`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/exceptions.py#L19)).

Related tests:
- [`test/test_search_service.py::test_configurable_sort_order_ascending`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/test/test_search_service.py#L195)
- [`test/test_search_service.py::test_configurable_sort_order_descending`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/test/test_search_service.py#L209)
- [`test/test_search_service.py::test_configurable_sort_order_via_payload`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/test/test_search_service.py#L223)
- [`test/test_search_service.py::test_configurable_sort_order_invalid_value_raises_validation_error`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/test/test_search_service.py#L237)
- [`test/test_search_service.py::test_configurable_sort_order_in_handler`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/test/test_search_service.py#L251)
- [`test/test_search_service.py::test_ac06_strict_relevance_order`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/test/test_search_service.py#L90) (prueba de regresión de relevancia).

---

## 5. Pull Request Review
PR:
- [Pull Request #2](https://github.com/Torres-David/ADA-05-SPEC-DRIVEN/pull/2): Título `"commit"`, rama origen `Cambio-ADA-06` $\rightarrow$ `main`. Commit head [`24a3d32c`](https://github.com/Torres-David/ADA-05-SPEC-DRIVEN/commit/24a3d32c3e8cfb9f0221f85b4f3a8609a3ad2da5). Estado: `OPEN`, `mergeable_state: clean`.

Changed behavior:
- Soporte para parámetro `order` opcional (`"asc"` o `"desc"`, por defecto `"asc"`) para el desempate alfabético por nombre.
- Si `order="desc"`, se invierte el orden alfabético secundario (Z-A) preservando la jerarquía de coincidencia primaria.
- Validación de entradas no permitidas con excepción `ValidationError` (HTTP 400).
- Soporte en CLI con argumento `--order {asc,desc}`.
- Reflejo del metadato `"order"` en las respuestas estructuradas.

Changed files:
- 9 archivos (+369 / -25 líneas): [`README.md`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/README.md), [`TASKS.md`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/TASKS.md), [`docs/Trazabilidad.md`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/docs/Trazabilidad.md), [`pytest.ini`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/pytest.ini), [`src/cli.py`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/cli.py), [`src/handler.py`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/handler.py), [`src/search_services.py`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/search_services.py), [`test/customers.json`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/test/customers.json), [`test/test_search_service.py`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/test/test_search_service.py).

Tests:
- 5 nuevas pruebas unitarias añadidas en `test/test_search_service.py`. Cobertura total de 47 tests automatizados pasando en 0.10s.

Observations:
- Cobertura exhaustiva de caminos felices, casos de borde e integración con el handler.
- Riguroso respeto a la metodología SDD actualizando especificación, tareas y trazabilidad en el mismo changeset.
- Compatibilidad hacia atrás garantizada manteniendo el valor `"asc"` por defecto.

Risks:
- Ordenamiento en dos llamadas sucesivas `.sort()` en [`src/search_services.py`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/search_services.py#L162-L167). Aunque Timsort es estable, tiene costo $2 \times O(N \log N)$ y es menos intuitivo que una clave de ordenamiento compuesta.
- Duplicación de datos entre `src/customers.json` y `test/customers.json`, susceptible a desincronización futura.

Questions:
- ¿Se reescribirá el mensaje del commit y título del PR a algo descriptivo (e.g. `feat(search): configurable sort order`) antes de mezclar a `main`?
- ¿El ordenamiento por diseño debe limitarse exclusivamente al nombre o se prevé ordenar por correo?

Potential defects:
- Inconsistencia de contrato en [`src/handler.py`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/handler.py#L96-L103): cuando el `RateLimiter` rechaza una solicitud con HTTP 429, la respuesta JSON omite el campo `"order"`, a diferencia de los códigos 200, 400 y 404.

---

## 6. Traceability
### Issue → Requirement/Spec → PR → Code → Test

| Issue / Need | Requirement / Spec | PR                                                     | Code / Files | Test / Evidence | Covered / Gap |
| :--- | :--- |:-------------------------------------------------------| :--- | :--- | :--- |
| **Issue #1**: Filtro orden asc/desc | `SPEC.md` Search Rules, `TASKS.md` T-07, `docs/Trazabilidad.md` FR-Sort | **PR #2** (Inferido) | `src/search_services.py`, `src/handler.py`, `src/cli.py` | `test_search_service.py` (5 tests de orden) | **Covered** (Gap: PR sin link `Closes #1`, respuesta 429 omite `order`) |
| **Need FR-01/02**: Case-insensitive y acentos | `REQUIREMENTS.md` FR-01, FR-02, `SPEC.md` AC-01, AC-02 | Rama base `main` (Inferido)            | `src/search_services.py` (`normalize_text`) | `test_ac01_*`, `test_ac02_*` | **Covered** |
| **Need FR-03**: No encontrado HTTP 404 | `REQUIREMENTS.md` FR-03, `SPEC.md` Error Handling | Rama base `main` (Inferido)                            | `src/search_services.py`, `src/exceptions.py` | `test_fr03_not_found_*`, `test_customer_not_found_*` | **Covered** |
| **Need FR-04/06**: Búsqueda por email $\ge 3$ caracteres | `REQUIREMENTS.md` FR-04, FR-06, `SPEC.md` AC-04 | Rama base `main` (Inferido*)            | `src/search_services.py` (`_match_email_partial`) | `test_ac04_email_*`, `test_email_search_*` | **Covered** |
| **Need FR-05**: Protección datos sensibles | `REQUIREMENTS.md` FR-05, `SPEC.md` AC-05 | Rama base `main` (Inferido)            | `src/customer.py` (`to_dict`) | `test_sensitive_fields_omitted_from_dict` | **Covered** |
| **Need AC-06**: Jerarquía de relevancia 6 niveles | `SPEC.md` AC-06 | Rama base `main` (Inferido)            | `src/search_services.py` (`_classify_match_priority`) | `test_ac06_strict_relevance_order` | **Covered** |
| **Need NFR-01**: Latencia p95 $\le$ 300 ms @ 50 req/s | `REQUIREMENTS.md` NFR-01 | Rama base `main` (Inferido)            | `src/handler.py`, `src/search_services.py` | `test_nfr01_p95_latency_*` | **Covered** |
| **Need NFR-02**: Rate limit 30 req/min (HTTP 429) | `REQUIREMENTS.md` NFR-02 | Rama base `main` (Inferido)            | `src/handler.py` (`RateLimiter`), `exceptions.py` | `test_nfr02_rate_limiting_*` | **Covered** |
| **Need NFR-03**: Accesibilidad WCAG 2.1 AA | `REQUIREMENTS.md` NFR-03 | —                                                      | — | — | **Excluido por Alcance** (Aplicación 100% consola CLI) |

---

## 7. Permission Review
Authentication:
- Autenticación mediante **Fine-Grained Personal Access Token (PAT)** vinculado a la cuenta `Torres-David`.

GitHub token permissions:
- Restricción estricta al repositorio `Torres-David/ADA-05-SPEC-DRIVEN` (*Only select repositories*).
- Permisos configurados exclusivamente en lectura: `Contents: Read-only`, `Issues: Read-only`, `Pull requests: Read-only`.

MCP read-only:
- Servidor `github-readonly` activo en modo de solo lectura forzado.

Enabled toolsets:
- `repos`, `issues`, `pull_requests`.

Write capabilities exposed:
- **Ninguna (0 herramientas de escritura)**. Bloqueadas en los esquemas expuestos al agente (`create_issue`, `push_files`, `comment_pr`, etc. no están disponibles).

---

## 8. Security Notes
- **Credential exposure:** El PAT reside exclusivamente en variables de entorno seguras inyectadas al proceso MCP; nunca se imprime en transcripciones, reportes ni código fuente.
- **Prompt injection:** Si descripciones de issues o PRs contuvieran instrucciones hostiles, el agente carece de herramientas sintácticas para ejecutar mutaciones remotas, y la API de GitHub denegaría con HTTP 403 cualquier escritura.
- **Excess permissions:** Aplicación rigurosa del Principio de Mínimo Privilegio. Sin permisos de administración, eliminación ni modificación de workflows/acciones.
- **Repository scope:** El alcance está limitado al repositorio del proyecto, previniendo fuga de datos hacia otros repositorios personales o corporativos.

---

## 9. Human Review
What did you verify yourself?
- Se ejecutó y verificó en terminal local la suite completa de pruebas (`pytest` arrojando 47 pasadas en 0.10s).
- Se comprobó manualmente la ejecución del CLI con el flag `--order desc` y `--order asc`.
- Se inspeccionaron línea por línea los diffs y parches remotos obtenidos a través de `pull_request_read`.
- Se validó la estabilidad del algoritmo Timsort de Python en `search_services.py` para asegurar que el orden inverso por nombre no corrompa la jerarquía de coincidencia.

What AI conclusions did you reject or modify?
- **Rechazo de categorización como "Filtro":** A pesar de que el Issue #1 se titulaba "filtro por orden", se rechazó la interpretación de que se tratara de un filtro condicional excluyente de registros. Se clarificó que se trata de **ordenamiento (*sorting*)** del desempate dentro de los niveles de relevancia.
- **Rechazo de inversión global de resultados:** Se descartó una inversión ciega de la lista (`results.reverse()`), ya que habría colocado coincidencias por subcadena por delante de coincidencias exactas, violando gravemente [`AC-06`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/SPEC.md#L52).
- **Explicitación de la inferencia Issue $\leftrightarrow$ PR:** Se corrigió cualquier asunción de que el PR #2 estuviera formalmente vinculado al Issue #1 en GitHub, clasificándolo con rigor metodológico como una **inferencia técnica comprobada**.

---

## 10. Conclusion
What did MCP add to the engineering workflow?
- **Acceso Directo y Determinista:** Permitió consultar la fuente de la verdad en GitHub (Issues, PRs, ramas y diffs) directamente desde el contexto de razonamiento del agente, eliminando la necesidad de alternar manualmente entre navegadores y terminales.
- **Auditoría y Trazabilidad sin Fricción:** Facilitó la comparación inmediata entre la especificación local y los cambios remotos, detectando gaps de metadatos y validando la consistencia entre requisitos, código y pruebas.
- **Seguridad Garantizada por Diseño:** Demostró la efectividad de una arquitectura multicapa de solo lectura, donde la productividad del agente se maximiza sin riesgo de escrituras o alteraciones no autorizadas en el repositorio remoto.
