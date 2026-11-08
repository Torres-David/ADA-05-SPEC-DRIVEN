# Technical Report — Task Under Test (CR-01) — AFTER AGENT RUN

## Clarification Questions Requested by the Agent
- **None requested.** El contexto del proyecto, los límites arquitectónicos y las especificaciones provistas en `REQUIREMENTS.md`, `SPEC.md`, `ARCHITECTURE.md`, `TASKS.md`, `docs/REPO_MAP.md`, `AGENTS.md` y `TASK_UNDER_TEST.md` proporcionaron requisitos completos, no ambiguos y ejecutables para implementar la solicitud de cambio de manera autónoma y segura.

---

## Files Explored to Understand the Repository
1. `REQUIREMENTS.md`: Requerimientos funcionales (`FR-01` a `FR-06`) y no funcionales (`NFR-01` latencia p95 $\le$ 300 ms, `NFR-02` rate limiting de 30 req/min por usuario, `NFR-03` accesibilidad WCAG 2.1 AA).
2. `SPEC.md`: Modelo de dominio `Customer`, reglas de prioridad en coincidencia (1: nombre exacto, 2: correo exacto, 3: prefijo nombre, 4: prefijo correo, 5: subcadena nombre, 6: subcadena correo), criterios de aceptación (`AC-01` a `AC-06`) y casos de borde.
3. `ARCHITECTURE.md`: Arquitectura por capas (`Handler` $\to$ `Service` $\to$ `Domain` / `Repository`), flujo de información y responsabilidades.
4. `TASKS.md`: Historial de tareas de backlog (`T-01` a `T-07`).
5. `docs/REPO_MAP.md`: Índice centralizado de navegación del repositorio con puntos de entrada, suites de prueba, documentos de especificación y archivos protegidos.
6. `TASK_UNDER_TEST.md`: Especificación de la solicitud de cambio `CR-01` (incorporación del parámetro opcional `search_field` con valores `'all'`, `'name'`, `'email'`).
7. `AGENTS.md`: Instrucciones del repositorio, fuentes de verdad, comandos estándar, reglas de cambio y definición de terminado (*Definition of Done*).
8. `GEMINI.md`: Adaptador de agente que delega a `AGENTS.md`.
9. `src/exceptions.py`: Jerarquía de excepciones de dominio (`CustomerSearchException`, `EmptyQueryError`, `ValidationError`, `CustomerNotFoundError`, `DatabaseError`, `RateLimitExceededError`).
10. `src/customer.py`: Entidad de dominio `Customer` con propiedades `id`, `nombre`/`name` y `email`.
11. `src/customer_repository.py`: Repositorio desacoplado para carga de clientes desde archivo JSON.
12. `src/customers.json`: Base de datos de prueba en memoria con 52 registros únicos.
13. `src/search_services.py`: Servicio central de búsqueda, reglas de prioridad, filtrado por ámbito (`search_field`), normalización de texto y paginación.
14. `src/handler.py`: Capa de recepción de solicitudes, control de rate limiting por ventana deslizante (NFR-02) e inyección a servicio.
15. `src/cli.py`: Interfaz de línea de comandos con soporte para argumentos `--search-field`, `--order`, paginación y modo interactivo.
16. `test/test_customer.py`: Pruebas unitarias de entidad y serialización.
17. `test/test_customers_data.py`: Pruebas de integridad del conjunto de datos semilla.
18. `test/test_nfr.py`: Pruebas de latencia p95 y aislamiento de rate limiting.
19. `test/test_search_service.py`: Pruebas de criterios de aceptación y nueva suite para `CR-01`.
20. `test/test_validation_and_errors.py`: Pruebas de captura de excepciones y respuestas HTTP (400, 404, 500).
21. `test/test_check_repo_contract.py`: Pruebas de guardrails contractuales del repositorio.
22. `scripts/verify_repo.py`: Script determinista unificado de validación del repositorio.
23. `scripts/check_repo_contract.py`: Validador automático de guardrails de contrato.

---

## Incorrect Assumptions
- **Ninguna.** Gracias a las reglas explícitas de `AGENTS.md` y la información provista en `docs/REPO_MAP.md`, no se realizaron suposiciones erróneas sobre terminadores de línea (se preservó CRLF nativo en Windows), no se ejecutaron comandos de inspección git no autorizados, y la semántica de precedencia de `TASK_UNDER_TEST.md` fue respetada directamente.

---

## Failed or Unknown Commands
- **Ninguno.** Todos los comandos ejecutados concluyeron con éxito según su propósito previsto. El comando de prueba de CLI con parámetro inválido (`python src/cli.py "emp" --search-field invalid`) retornó el código de salida esperado de validación (`error: argument --search-field: invalid choice: 'invalid'`). No hubo fallos en herramientas de edición ni violaciones de permisos.

---

## Out-of-Scope Files Modified
- **Ninguno.** Únicamente se modificaron los archivos en alcance requeridos para implementar el cambio `CR-01`, su documentación y la evidencia solicitada:
  - `src/search_services.py`: Implementación de lógica de ámbito `search_field`, validación de valores permitidos y propagación de resultados.
  - `src/handler.py`: Soporte y propagación de parámetro `search_field` en método `handle()`.
  - `src/cli.py`: Incorporación del argumento `--search-field {all,name,email}` y formateo de resultados de consola.
  - `test/test_search_service.py`: Incorporación de 8 nuevas pruebas automatizadas cubriendo todos los criterios de verificación de `CR-01`.
  - `TASKS.md`: Registro de la tarea `T-08 Scoped search field (CR-01)`.
  - `README.md`: Documentación actualizada de uso en CLI, uso programático y reglas de negocio.
  - `results/implicit-knowledge.md`: Documento de conocimiento implícito identificado, remediado y clasificado.
  - `results/after-agent-run.md`: Informe técnico de ejecución y rúbrica comparativa AFTER.

---

## Tests/Validations Executed or Skipped

### 1. Pre-Change Baseline Validation
- **Comando ejecutado**: `pytest -v` y `python scripts/verify_repo.py`
- **Resultado inicial**: 69 pruebas aprobadas en 0.20s (100% PASS), linter compileall limpio, 7 guardrails aprobados.

### 2. Post-Change Automated Test Suite
- **Comando ejecutado**: `pytest -v`
- **Resultado final**: 77 pruebas aprobadas en 0.24s (0 fallidas, 0 omitidas, 0 regresiones).
- **Desglose de pruebas por archivo**:
  - `test/test_check_repo_contract.py`: 8 pasadas (guardrails de contrato)
  - `test/test_customer.py`: 9 pasadas (entidad de dominio)
  - `test/test_customers_data.py`: 5 pasadas (integridad de datos semilla)
  - `test/test_nfr.py`: 3 pasadas (NFR-01 rendimiento p95 y NFR-02 rate limit)
  - `test/test_search_service.py`: 29 pasadas (21 preexistentes + 8 nuevas de `CR-01`)
  - `test/test_validate_review_report.py`: 14 pasadas (validador de reporte de PR)
  - `test/test_validation_and_errors.py`: 9 pasadas (manejo de errores y códigos HTTP)

### 3. New Tests Added for CR-01
- `test_search_field_name_scoping`: Verifica que con `search_field='name'`, la consulta evalúa únicamente contra el nombre del cliente y excluye coincidencias exclusivas de correo.
- `test_search_field_email_scoping`: Verifica que con `search_field='email'`, la consulta evalúa únicamente contra el correo electrónico y excluye coincidencias exclusivas de nombre.
- `test_search_field_all_and_omitted_matches_both`: Verifica que con `search_field='all'` u omitido se evalúan ambos campos, preservando compatibilidad hacia atrás.
- `test_search_field_via_payload_dictionary`: Verifica la recepción y procesamiento de `search_field` dentro del diccionario `request_payload`.
- `test_search_field_invalid_value_raises_validation_error`: Verifica que valores no soportados lanzan `ValidationError` y retornan código HTTP 400.
- `test_search_field_in_handler_invocation`: Verifica que `CustomerSearchHandler.handle()` acepta y propaga `search_field` por argumento y por payload.
- `test_search_field_scoping_with_seed_database`: Verifica el filtrado por ámbito sobre la base de datos real de 52 clientes (el término `'emp'` coincide bajo `'email'` y `'all'`, pero retorna 404 bajo `'name'`).
- `test_search_field_case_insensitivity_and_none_default`: Verifica normalización de mayúsculas/minúsculas y espacios en `search_field` (ej. `'  NAME  '` $\to$ `'name'`) y valor predeterminado `'all'` ante `None`.

### 4. CLI Runtime Validations Executed
- `python src/cli.py "Carlos" --search-field name` $\to$ **HTTP 200**, retorna Carlos Santana.
- `python src/cli.py "emp" --search-field name` $\to$ **HTTP 404**, excluye coincidencia exclusiva de correo Soporte TI.
- `python src/cli.py "emp" --search-field email` $\to$ **HTTP 200**, retorna Soporte TI (`soporte.ti@empresa.com`).
- `python src/cli.py "emp" --search-field all` $\to$ **HTTP 200**, retorna Soporte TI.
- `python src/cli.py "emp" --search-field invalid` $\to$ **Exit Code 1**, opción inválida rechazada por `argparse`.

### 5. Repository Contract & Unified Verification Pipeline
- **Comando ejecutado**: `python scripts/verify_repo.py`
- **Etapa [1/3] Pruebas**: 77 pruebas pasadas en 0.21s.
- **Etapa [2/3] Lint**: `python -m compileall -q src test scripts` completado exitosamente.
- **Etapa [3/3] Guardrails**: `scripts/check_repo_contract.py` aprobó los 7 guardrails:
  - `[PASS]` Archivos y directorios esenciales presentes
  - `[PASS]` Trazabilidad de requerimientos en `SPEC.md`
  - `[PASS]` Comandos estándar y contrato en `AGENTS.md`
  - `[PASS]` Escaneo de patrones sensibles y secretos
  - `[PASS]` Integridad de enlaces en `docs/REPO_MAP.md`
  - `[PASS]` Integridad y no duplicidad de base de datos semilla
  - `[PASS]` Contratos de adaptadores de agentes (`GEMINI.md`, `CLAUDE.md`)
- **Resultado final**: `VERIFY_REPO: PASS`.

### 6. Skipped Tests
- **Ninguno.** Las 77 pruebas automáticas y todas las verificaciones deterministas fueron ejecutadas y pasaron al 100%.

---

## Final Result: PASS / PARTIAL / FAIL
**PASS**

Todos los criterios de aceptación y requerimientos de `TASK_UNDER_TEST.md` (`CR-01`) se cumplieron en su totalidad con cero regresiones y verificación reproducible.

---

## Indicadores Comparativos (BEFORE vs AFTER)

| Indicador | BEFORE | AFTER |
|---|---|---|
| **Clarification questions** | 0 (Ninguna requerida) | 0 (Ninguna requerida — contexto autosuficiente) |
| **Failed / unknown commands** | 3 (`edit_file` por CRLF, `git status` denegado, CLI invalid) | 0 (Ningún fallo de herramienta o ejecución) |
| **Incorrect assumptions** | 3 (Suposición de LF, suposición de git, suposición de scoping en payload) | 0 (Preservación de CRLF, comandos autorizados, alcance exacto) |
| **Out-of-scope files modified** | 0 | 0 (Solo archivos en alcance y documentación requerida) |
| **Validations executed correctly** | Parcial (solo `pytest` manual, sin guardrails automáticos de repositorio) | Completa (`pytest` 77/77, `compileall`, CLI y pipeline unificado `verify_repo.py`) |
| **Final result PASS / PARTIAL / FAIL** | PASS | PASS |
| **Qualitative observation** | Fricción por terminadores CRLF, advertencias de permisos en comandos git y ausencia de pipeline unificado de verificación. | Ejecución autónoma, limpia y fluida; descubrimiento inmediato de archivos, cero fricciones en herramientas y verificación determinista en un solo comando. |
| **Discoverability** | Descubrimiento manual mediante prompts; ausencia de mapa centralizado del repositorio; ambigüedad entre `TASKS.md` y `TASK_UNDER_TEST.md`. | **Óptima / Autónoma**: `docs/REPO_MAP.md` y `AGENTS.md` indexan puntos de entrada, fuentes de verdad, suites de prueba y reglas operativas sin intervención humana. |
| **Implicit Knowledge** | Conocimiento tribal no documentado (terminadores CRLF, prohibición de comandos git, prevalencia de `TASK_UNDER_TEST.md`, ausencia de dependencias formales). | **Explícito y Remediado**: Documentado en `results/implicit-knowledge.md` y formalizado en `AGENTS.md`, `requirements.txt` y `scripts/check_repo_contract.py`. |
| **Clasificación de mejoras** | Brechas no clasificadas y dispersas en múltiples archivos. | Cada remediación categorizada explícitamente: **Context**, **Navigation**, **Executable Knowledge**, **Guardrail**, **Test**, **CI Check**, **Human Gate**. |
| **CI / shared checks** | Inexistencia de pipeline unificado o script local ejecutable equivalente a CI. | `scripts/verify_repo.py` implementa el contrato ejecutable idéntico para desarrollo local e integración continua (test, lint, guardrails). |

---

## Evaluación de Madurez del Repositorio (Rúbrica AFTER)

Repetición estricta de la rúbrica original (mismas 8 dimensiones y ponderaciones):

| Dimension | Score 0-5 | Weighted | Evidence | Improvement |
|---|---:|---:|---|---|
| **Entry Point & Navigation** | 5 | 15.0 / 15 | `AGENTS.md` define el orden de lectura estricto; `docs/REPO_MAP.md` centraliza el mapa de todo el repositorio (puntos de entrada, tests, guías de cambio y archivos protegidos). La integridad de enlaces es validada automáticamente por `scripts/check_repo_contract.py`. | **Navigation** |
| **Agent Instructions** | 5 | 15.0 / 15 | `AGENTS.md` incluye comandos estándar (Install, Run, Test, Lint, Verify), reglas operativas explícitas (prohibición de git no autorizado, preservación de CRLF), condiciones de parada y Definition of Done no ambigua. `GEMINI.md` delega limpiamente sin duplicar requerimientos. | **Context** / **Guardrail** |
| **Build / Run / Test** | 5 | 15.0 / 15 | `requirements.txt` declara dependencias formales. Script determinista unificado `scripts/verify_repo.py` (y `scripts/verify_repo.sh`) ejecuta en un solo paso pruebas (`pytest -q`), compilación/lint (`compileall -q`) y guardrails (`check_repo_contract.py`). Cero configuración manual requerida. | **Executable Knowledge** / **CI Check** |
| **Architecture Boundaries** | 5 | 10.0 / 10 | `ARCHITECTURE.md` define claramente las capas (`Handler` $\to$ `Service` $\to$ `Domain` / `Repository`), flujo de datos y DTOs autorizados. `docs/REPO_MAP.md` establece límites negativos explícitos ("Do Not Edit Directly") para proteger especificaciones y secretos. | **Guardrail** / **Context** |
| **Requirements & Traceability** | 5 | 10.0 / 10 | Requerimientos (`FR-01`..`FR-06`, `NFR-01`..`NFR-03`), criterios de aceptación (`AC-01`..`AC-06`) y tareas (`T-01`..`T-08`, `CR-01`) están completamente interconectados. Trazabilidad validada de forma automatizada por `scripts/check_repo_contract.py`. | **Test** / **Guardrail** |
| **Automation & Guardrails** | 5 | 10.0 / 10 | Validador contractual automatizado `scripts/check_repo_contract.py` con 7 guardrails deterministicos (archivos obligatorios, trazabilidad de especificaciones, comandos estándar, escáner de patrones de secretos, integridad de enlaces en REPO_MAP, esquema de base de datos semilla y contratos de adaptadores). Respaldado por `test_check_repo_contract.py`. | **Guardrail** / **CI Check** |
| **Testability & Evidence** | 5 | 15.0 / 15 | Suite automatizada de 77 pruebas ejecutándose en ~0.21s con 100% de éxito y cero regresiones. Cubre dominio, integridad de datos, criterios de aceptación, rendimiento p95 $\le$ 300 ms, rate limiting de 30 req/min, reporte de PR y guardrails de repositorio. Evidencia generada de forma verificable. | **Test** |
| **Safety & Permissions** | 5 | 10.0 / 10 | Escaneo activo de secretos y tokens en código; prohibición expresa de comandos git no solicitados; protección estricta de `.env`, `REQUIREMENTS.md` y `SPEC.md`; sanitización de DTOs para evitar filtración de atributos sensibles (`password_hash`, `tax_id`). | **Guardrail** / **Human Gate** |

---

### **TOTAL AFTER: 100.0 / 100**

### **DELTA: AFTER (100.0) - BEFORE (59.0) = +41.0 points**
