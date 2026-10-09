# Comparativa de Diseño: Skill Propia (`reviewing-pull-requests`) vs. Skill Profesional (`code-review-and-quality`)

## Introducción

Ambas Skills fueron ejecutadas de forma independiente sobre el mismo cambio: el **Pull Request #4** ( commit [`6212ff2`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/commit/6212ff28d62d9f1cad7a82bc85b831b3aea8dd5c)), que implementa el ordenamiento configurable en la búsqueda de clientes ([`T-07`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/TASKS.md#L32)). La comparación se sustenta en la evidencia empírica generada en los reportes [`results/pr-readiness-review.md`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/results/pr-readiness-review.md) y [`results/professional-skill-review.md`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/results/professional-skill-review.md).

---

## Tabla Comparativa de Dimensiones

| Dimensión | Tu Skill (`reviewing-pull-requests`) | Profesional (`code-review-and-quality`) | Conclusión |
| :--- | :--- | :--- | :--- |
| **Trigger / routing** | **Especializado en PRs de GitHub:** Enruta exclusivamente revisiones formales de PRs, branches o diffs de repositorio vinculados a requerimientos (`REQUIREMENTS.md`/`SPEC.md`). Excluye explícitamente implementar código, comentar o explicar conceptos Git. | **Universal pre-merge:** Se activa ante cualquier cambio antes de entrar a `main`: PRs, diffs pegados en línea en el chat, código de agentes o humanos, refactorizaciones y bug fixes post-mortem. | La profesional ofrece mayor versatilidad de entrada (e.g. diffs sin PR en GitHub); la propia es más precisa para compuertas formales de CI/CD. |
| **Scope / boundaries** | **Aislamiento estricto (*Scope Isolation*):** En v1.0.1 prohíbe examinar cambios locales sin comitear (`git status`) o carpetas ajenas. Prohíbe mutaciones en GitHub y se frena si `REQUIREMENTS.md` y `SPEC.md` colisionan. | **Gobierno de calidad y anti-inflación:** Limita tamaños de cambio (~100-300 líneas), exige preguntar antes de borrar código muerto y prohíbe editar lockfiles a mano. No restringe la lectura del espacio de trabajo. | Tu Skill previene la dispersión del agente (*context drift*); la profesional previene la acumulación de deuda técnica y cambios sobredimensionados. |
| **Workflow depth** | **Lineal y determinista (10 pasos):** Proceso rígido acoplado a un script de validación sintáctica (`validate_review_report.py`) y una plantilla estructurada (`review_report_template.md`). | **Heurístico de ingeniería (5 fases):** Contexto $\rightarrow$ Tests primero (inversión TDD) $\rightarrow$ Implementación en 5 ejes $\rightarrow$ Categorización priorizada $\rightarrow$ Verificación de la verificación. | Tu Skill destaca en conformidad determinista y automatizable; la profesional aporta un razonamiento de ingeniería mucho más profundo y reflexivo. |
| **Correctness** | **Trazabilidad formal SDD:** Verifica que cada cambio mapee exactamente a un criterio funcional (`FR-01` a `FR-06`, `AC-01` a `AC-06`, `T-07`). Prohíbe inventar reglas de negocio no documentadas. | **Robustez funcional y casos de borde:** Verifica especificación, pero profundiza en rutas de error no anticipadas, condiciones de carrera, errores de límites (*off-by-one*) y simetría de contratos. | Tu Skill asegura que no haya desvíos de producto; la profesional analiza con mayor agudeza la integridad del runtime ante entradas inesperadas. |
| **Architecture** | **Validación estricta de capas:** Comprueba el respeto a las capas de [`ARCHITECTURE.md`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/ARCHITECTURE.md) (Handler $\rightarrow$ Service $\rightarrow$ Domain $\rightarrow$ Repository). | **Diseño y Remedios Estructurales:** Evalúa reducción vs reubicación de complejidad, fugas en módulos compartidos, tipos explícitos, y prescribe *movimientos de diseño* concretos. Detecta duplicación de fixtures JSON. | La profesional no solo juzga la arquitectura, sino que ofrece alternativas de rediseño y previene la proliferación de abstracciones estériles. |
| **Security** | **Checklist defensivo básico:** Revisa ausencia de secretos, permisos mínimos y validación elemental de parámetros en la frontera del PR. | **Eje formal y modelado de amenazas:** Audita sanitización de entradas, parametrización, codificación de salida, desconfianza de datos externos y enlaza a `security-and-hardening`. | La profesional integra la seguridad como disciplina de ciclo continuo; tu Skill se limita a una lista de verificación previa al merge. |
| **Performance** | **Verificación reactiva de NFR:** Se limita a comprobar que las pruebas automatizadas de rendimiento (`test_nfr.py` con p95 $\le$ 300 ms) pasen exitosamente. | **Análisis algorítmico proactivo:** Evalúa complejidad temporal ($O(N \log N)$), hot paths, asignaciones de memoria, paginación defensiva y enlaza a `performance-optimization`. | Tu Skill confía pasivamente en el resultado del test; la profesional analiza proactivamente el diseño asintótico del código. |
| **Tests / verification** | **Ejecución de suite (Pass/Fail):** Ejecuta `pytest -v` (61 tests pasando) y constata que existan pruebas para la nueva funcionalidad (`T-07`). | **Verificación activa por mutación:** Exige *revisar tests antes del código* y aplicar **pruebas de mutación experimental** (invertir condiciones para confirmar que la suite falle), además de exigir evidencia visual en UI. | La profesional prueba la eficacia real de los tests contra regresiones; tu Skill se conforma con que la suite actual esté en verde. |
| **Severity model** | **Taxonomía de PR (4 niveles):** `MUST FIX`, `SHOULD FIX`, `OPTIONAL`, `Human decision required`. Muy orientada al flujo de revisión de pull requests. | **Taxonomía estandarizada con prefijos:** `Critical:`, `Required` (sin prefijo), `Nit:`, `Optional:`/`Consider:`, `FYI`. Incluye *Presumptive Blockers* y regla *Lead with what matters*. | El modelo profesional reduce la fatiga del desarrollador jerarquizando por impacto e indicando claramente qué comentarios puede ignorar el autor. |
| **Human review** | **Pausa y entrega:** Emite el reporte, señala los puntos que requieren decisión humana y detiene la ejecución a la espera de instrucciones. | **Filosofía de decisión y mediación:** Brinda un estándar de aprobación incremental (*"approve when it improves code health"*), combate la adulación (*anti-sycophancy*) y define jerarquía para disputas. | Tu Skill cede el control pasivamente; la profesional dota al revisor humano de criterios objetivos para desbloquear debates técnicos. |
| **References / composition** | **Autocontenida localmente:** Utiliza referencias internas (`references/review_checklist.md`, `severity_guide.md`, `scripts/validate_review_report.py`). | **Composición modular de red:** Conecta dinámicamente con Skills especializadas (`security-and-hardening`, `performance-optimization`, `constraint-driven-development`) y orquestación multi-modelo. | Tu Skill opera como un bloque autónomo monolítico; la profesional actúa como un orquestador dentro de un ecosistema colaborativo. |
| **Reusability** | **Altamente contextual:** Diseñada para el entorno docente/metodológico de Spec-Driven Development en UADY-IS-AI, acoplada a la estructura del repositorio. | **Universal y agnóstica:** Aplicable a cualquier stack tecnológico, lenguaje de programación, equipo de ingeniería o repositorio corporativo. | La profesional es un activo reutilizable universal; tu Skill es una herramienta especializada de alto rendimiento para el contexto del proyecto. |

---

## Análisis de Preguntas Clave

### 1. ¿Qué hace la Skill profesional que tu Skill no contempló?

Al contrastar la ejecución sobre el PR #4, la Skill profesional introdujo capacidades de alto nivel que estaban ausentes en `reviewing-pull-requests`:

1. **Pruebas de Mutación Experimental en Revisión de Tests (*Step 2*):** En lugar de solo verificar que existan tests y pasen, la Skill instruye intervenir activamente el código invirtiendo una condición (e.g. forzar `clean_order == "desc"` a `clean_order == "asc"`) para constatar empíricamente si la suite atrapa el cambio. Si el test queda verde, se levanta un hallazgo de cobertura insuficiente.
2. **Catálogo de Remedios Estructurales Nombrados (*Structural Remedies*):** Cuando señala problemas de complejidad, obliga al agente a prescribir la refactorización exacta (e.g., separar orquestación de lógica, colapsar ramas duplicadas, eliminar wrappers pasantes) en lugar de emitir juicios vagos como "este código es confuso".
3. **Auditoría de Higiene en Versionamiento y Commits:** Detectó inmediatamente el título genérico `"Revertir el revert..."` y los commits `"commit"`, citando explícitamente que los cambios deben tener descripciones que se sostengan por sí mismas en el historial de Git.
4. **Disciplina Atómica de Dependencias y Lockfiles:** Instrucciones minuciosas para evitar actualizaciones masivas (*bulk bumps*), exigir lectura de changelogs y prohibir terminantemente la manipulación manual de lockfiles.
5. **Estándar de Aprobación Incremental (*Continuous Health Improvement*):** El principio explícito de *"aprobar un cambio si definitivamente mejora la salud general del código, incluso si no es perfecto"*, desarticulando bloqueos innecesarios por preferencias de estilo del revisor.

---

### 2. ¿Qué elementos de tu Skill son más específicos al curso/proyecto y conviene conservar?

Existen salvaguardas y mecanismos dentro de `reviewing-pull-requests` que responden directamente a los objetivos de Spec-Driven Development (SDD) y que deben preservarse:

1. **Aislamiento Estricto de Alcance (*Scope Isolation* en v1.0.1):** En la iteración v1.0.0, el agente cayó en dispersión al inspeccionar el estado de la copia de trabajo local (`git status`, cambios no comiteados) y directorios ajenos al PR. La directiva agregada en v1.0.1 que confina la lectura al diff del PR, la especificación y la ejecución de pruebas es crucial para evitar que el agente alucine con archivos de trabajo no integrados.
2. **Validación Determinista de Reportes mediante Script (`scripts/validate_review_report.py`):** Mientras que la Skill profesional confía en que el LLM formatee bien su respuesta en markdown, tu Skill ejecuta un script en Python que valida sintácticamente que el reporte contenga las secciones obligatorias (`MUST FIX`, `SHOULD FIX`, `OPTIONAL`, etc.). Esto garantiza calidad determinista en pipelines CI/CD.
3. **Frontera de Incompatibilidad Normativa (*Spec Conflict Boundary*):** La regla mandataria de detenerse de inmediato si [`REQUIREMENTS.md`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/REQUIREMENTS.md) y [`SPEC.md`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/SPEC.md) discrepan. En SDD, un agente o revisor nunca debe resolver por su cuenta una inconsistencia en las reglas de negocio de la empresa.
4. **Trazabilidad Bidireccional de Requerimientos:** Exigir que cada cambio de comportamiento mapee numéricamente a un Functional Requirement (FR) o Acceptance Criteria (AC).

---

### 3. ¿Qué agregarías a una versión 2 de tu Skill?

Para evolucionar `reviewing-pull-requests` a una versión 2.0.0 de clase mundial sin perder su enfoque en SDD, incorporaría:

1. **Taxonomía de Severidad Estandarizada con Prefijos:** Adoptar el esquema `Critical:`, `Required:`, `Nit:`, `Consider:` y `FYI`, manteniendo la agrupación por bloques pero etiquetando cada hallazgo para que el autor distinga inmediatamente lo cosmético de lo arquitectónico.
2. **Compuerta de Dimensionamiento de Cambios (*Change Sizing Gate*):** Añadir umbrales explícitos de revisión: rechazar o solicitar división obligatoria de PRs que superen las $\sim 300$ líneas de diff o que modifiquen archivos de más de $\sim 1000$ líneas sin descomponerlos previamente.
3. **Protocolo de Pruebas de Mutación para Tests Nuevos:** Exigir al agente que reporte evidencia de haber probado la sensibilidad de los nuevos tests unitarios (demostrando que fallan cuando se rompe la regla de negocio que pretenden proteger).
4. **Catálogo de Remedios Estructurales en la Checklist:** Integrar en `references/review_checklist.md` una sección de soluciones arquitectónicas sugeridas para que las observaciones de nivel `SHOULD FIX` siempre vayan acompañadas de una propuesta de código alternativa.
5. **Composición Explícita con Skills Complementarias:** Permitir que tu Skill invoque o cite formalmente a `security-and-hardening` o `performance-optimization` cuando el PR toque autenticación, datos sensibles o bucles masivos.

---

### 4. ¿Qué NO copiarías y por qué?

1. **NO copiaría la ausencia de validación determinista:** La Skill profesional no cuenta con ningún script que valide que el reporte emitido por el modelo cumpla con una estructura fija. Eliminar `scripts/validate_review_report.py` representaría una degradación en confiabilidad, ya que los LLMs pueden omitir secciones críticas inadvertidamente.
2. **NO copiaría el alcance de lectura irrestricto:** La Skill profesional no prohíbe explícitamente inspeccionar el árbol de trabajo local no comiteado. En entornos donde un agente tiene acceso al sistema de archivos local, esto causa que el LLM confunda cambios en progreso del desarrollador con el contenido real del Pull Request remoto (la falla observada en la iteración v1.0.0).
3. **NO copiaría la resolución implícita de ambigüedades:** La Skill profesional sugiere que el revisor o autor acuerden la solución en base a principios de ingeniería. En un entorno regulado por Spec-Driven Development, si una especificación es ambigua o contradictoria, la revisión debe frenar en seco y exigir clarificación al Product Owner / Humano, sin asumir interpretaciones libres.
4. **NO copiaría la dilución del entregable único:** La Skill profesional deja abierta la salida (puede ser un comentario en el chat o un checklist markdown). Mantener la exigencia de un archivo de reporte canónico en `results/` permite auditoría histórica y trazabilidad institucional.

---

### 5. ¿Cuál produjo hallazgos más accionables? Incluye dos ejemplos.

**Conclusión:** La Skill profesional (`code-review-and-quality`) produjo hallazgos **más accionables**, porque no se limitó a señalar la existencia de una discrepancia, sino que diagnosticó la causa raíz de ingeniería de software, evaluó el impacto en mantenibilidad futura y propuso la solución técnica exacta. Tu Skill identificó los problemas correctamente gracias a su checklist, pero sus recomendaciones fueron más superficiales.

#### Ejemplo 1: El doble ordenamiento `.sort()` en `search_services.py` (Líneas 163-167)
- **Tu Skill ([`results/pr-readiness-review.md`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/results/pr-readiness-review.md#L84-L94)):**
  - *Problema señalado:* "Se ejecutan dos pasadas de ordenamiento `.sort()` consecutivas... podría expresarse en un solo paso mediante una clave de ordenamiento compuesta."
  - *Acción recomendada:* "Refactorizar en un solo `.sort()` con tupla en futuros ciclos si se busca optimización micro."
  - *Limitación:* En Python, no es trivial ordenar una tupla con clave compuesta donde el primer elemento es ascendente y el segundo es un string descendente (`-item[1]` genera `TypeError`). La sugerencia de "una sola tupla" puede inducir a un bug.
- **Skill Profesional ([`results/professional-skill-review.md`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/results/professional-skill-review.md#L85-L95)):**
  - *Diagnóstico técnico:* Reconoció que la técnica de dos `.sort()` es válida gracias a la **estabilidad algorítmica garantizada de Timsort**, pero identificó que el riesgo real no es el rendimiento, sino la **mantenibilidad**: un futuro ingeniero sin contexto podría invertir el orden de ejecución o intentar colapsarlo rompiendo la estabilidad.
  - *Acción recomendada:* Documentar explícitamente la dependencia en la estabilidad de Timsort para orden mixto o encapsular el ordenamiento secundario en un helper nombrado y tipado (`_sort_by_relevance_and_name_desc`).
  - *Por qué es más accionable:* Protege al equipo contra regresiones futuras y ofrece una solución precisa y viable en Python.

#### Ejemplo 2: Asimetría en el contrato HTTP 429 en `handler.py` (Líneas 96-103)
- **Tu Skill ([`results/pr-readiness-review.md`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/results/pr-readiness-review.md#L62-L78)):**
  - *Problema señalado:* Cuando ocurre Rate Limiting (429), el diccionario omite `"order"`.
  - *Acción recomendada:* "Incluir `'order': order` en el diccionario de respuesta HTTP 429 dentro de `CustomerSearchHandler.handle()`."
- **Skill Profesional ([`results/professional-skill-review.md`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/results/professional-skill-review.md#L73-L83)):**
  - *Diagnóstico técnico:* Clasificó el hallazgo formalmente como `Required (no prefix)` bajo el eje de Arquitectura y Contratos de Interfaces, contrastándolo contra la definición de DTO autorizado en [`ARCHITECTURE.md`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/ARCHITECTURE.md). Explicó que la omisión de metadatos de contexto en respuestas de error de transporte rompe la deserialización tipada en clientes frontend/móviles que consumen el endpoint.
  - *Acción recomendada:* Proporcionó el fragmento de código de corrección exacto para homogeneizar el contrato de respuesta en `handler.py` preservando los campos contextuales sin comprometer la seguridad.
  - *Por qué es más accionable:* Vinculó el detalle sintáctico con el impacto sistémico en los consumidores del API y aportó la justificación de severidad requerida para priorizar el cambio antes del merge.
