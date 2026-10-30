# AI Usage & Audit Log (ADA-08) — Agent-Ready Repository

Este registro documenta las interacciones, decisiones críticas de ingeniería, adopciones y rechazos durante la auditoría, diseño y validación del repositorio *Agent-Ready* para ADA-08.

---

## Entradas Significativas de Auditoría e Interacción

| # | Etapa / Hito | Qué detectó / sugirió el agente | Decisión Humana / Validación | Impacto en el Repositorio |
|---|---|---|---|---|
| **1** | **Auditoría Inicial** | El agente detectó una puntuación basal de **59.0 / 100**, con severas brechas en *Automation & Guardrails* (1/5) y *Safety & Permissions* (2/5). Identificó que las reglas de `AGENTS.md` dependían solo de buena voluntad, no existía un mapa central de navegación y el entorno asumía dependencias preexistentes. | **Validado completamente.** Se corroboró que el repositorio carecía de un pipeline unificado de verificación y que cualquier modelo fallaría al intentar editar con terminadores LF sobre Windows CRLF o al ejecutar comandos git no acotados. | Establecimiento de la línea base en `REPOSITORY_READINESS_AUDIT.md` y priorización de las 3 áreas críticas de fricción. |
| **2** | **Diseño de AGENTS.md** | El agente sugirió inicialmente redactar un `AGENTS.md` exhaustivo que incluyera resúmenes de los requerimientos de negocio (`FR-01` a `FR-06`), diagramas de flujo y duplicación de reglas en `GEMINI.md` y `CLAUDE.md`. | **Sugerencias rechazadas y depuradas.** Se rechazó duplicar requerimientos en `AGENTS.md` para evitar el problema de desincronización (*split-brain*). Se acordó que `AGENTS.md` contenga solo meta-instrucciones (SoT, comandos estándar, *Change Rules*, *Stop Conditions* y DoD) y que los adaptadores solo deleguen hacia él. | `AGENTS.md` conciso y autoritativo; adaptadores específicos (`GEMINI.md`) limpios sin duplicaciones. |
| **3** | **Guardrail (Instrucción a Software)** | La directiva en lenguaje natural decía: *"No modificar SPEC.md ni REQUIREMENTS.md, no incluir secretos y no modificar archivos no relacionados"*. En la práctica, los agentes violan estas reglas si no hay un freno ejecutable. | **Conversión a software implementada.** Se diseñó [`scripts/check_repo_contract.py`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/scripts/check_repo_contract.py) conteniendo 7 guardrails automáticos en Python (presencia de archivos esenciales, trazabilidad de IDs de requerimientos en `SPEC.md`, validación de comandos en `AGENTS.md`, escáner regex de patrones de secretos, integridad de enlaces en `docs/REPO_MAP.md`, e integridad de `src/customers.json`). | Reglas de negocio y seguridad convertidas en código ejecutable con suite de pruebas en [`test/test_check_repo_contract.py`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/test/test_check_repo_contract.py). |
| **4** | **Ejecución AFTER** | Durante la implementación de `CR-01` (`search_field`), el agente navegó inmediatamente a los archivos exactos usando `docs/REPO_MAP.md`, respetó la preservación de terminadores CRLF, no ejecutó ningún comando git prohibido y validó todo con `python scripts/verify_repo.py`. | **Resultado verificado.** Cero preguntas de aclaración, cero comandos fallidos, cero suposiciones incorrectas, 77/77 pruebas aprobadas y puntuación perfecta de **100.0 / 100** (+41.0 puntos sobre el BEFORE). | Confirmación empírica de que la infraestructura *Agent-Ready* elimina la fricción operativa. |
| **5** | **Evaluación Final (Límites Humanos)** | El agente resolvió el cambio técnico y la verificación reproducible, pero consultó si era posible dar por cerrada la arquitectura de base de datos en memoria para el release final. | **Intervención humana indispensable.** Se ratificó que la definición de nuevos requerimientos de negocio, cambios en persistencia de producción, trade-offs de privacidad y la autorización de merge/deploy pertenecen exclusivamente al juicio humano (*Human Gate*). | Fronteras claras entre la autonomía de implementación del agente y la soberanía de decisión del equipo de ingeniería. |
| **6** | **Discoverability / Implicit Knowledge** | Se detectó que el conocimiento sobre terminadores de línea Windows CRLF (`\r\n`), la prohibición de comandos git y la precedencia de `TASK_UNDER_TEST.md` sobre `TASKS.md` residía únicamente en la memoria de los evaluadores. | **Formalización ejecutada.** Se creó [`results/implicit-knowledge.md`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/results/implicit-knowledge.md) documentando cada caso, riesgo y remediación, y se incorporó la regla de precedencia en `AGENTS.md` y `docs/REPO_MAP.md`. | Eliminación definitiva de información tribal no escrita. |
| **7** | **CI / Shared Checks** | El equipo requería asegurar que lo que prueba el agente en su sesión coincida exactamente con lo que evalúa un desarrollador humano y con lo que ejecuta el pipeline de integración continua. | **Unificación de contrato.** Se estableció el script determinista [`scripts/verify_repo.py`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/scripts/verify_repo.py) como contrato compartido para las tres entidades (Humano, Agente, CI), ejecutando `pytest -q`, `compileall -q` y `check_repo_contract.py`. | Garantía de paridad absoluta entre entornos locales y automatizados. |

---

## Reflexión Individual (13 Preguntas Fundamentales)

### 1. ¿Cuál fue el principal obstáculo para el agente en la ejecución BEFORE?
El principal obstáculo fue la **carencia de límites operativos y contratos de entorno explícitos**. Al operar sobre un repositorio Windows sin directivas de formato, el agente asumió terminadores de línea LF (`\n`), lo que ocasionó que operaciones de reemplazo de texto fallaran al chocar contra los terminadores CRLF (`\r\n`) del disco. De forma similar, la ausencia de una regla explícita sobre herramientas de control de versiones causó que el agente ejecutara `git status`, deteniendo la sesión por solicitud de permisos al usuario. Finalmente, la falta de un comando unificado de verificación obligó a inferir cómo validar el proyecto.

### 2. ¿Qué información tuvo que inferir el agente que un desarrollador experimentado ya conocía?
Un desarrollador familiarizado con el proyecto ya conocía tácticamente:
- Que `src/customers.json` correspondía a la base de datos simulada en memoria y era de solo lectura para búsquedas.
- Que no se debían correr comandos de inspección ni mutación de estado de git durante tareas de código.
- Que cuando existía un archivo `TASK_UNDER_TEST.md` activo (`CR-01`), este tenía precedencia inmediata sobre el backlog histórico en `TASKS.md`.
- Que el entorno local corría sobre Windows y que preservar la codificación y terminadores nativos era fundamental para no corromper archivos.

### 3. ¿Qué mejora produjo el mayor impacto y por qué?
La dupla conformada por **[`docs/REPO_MAP.md`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/docs/REPO_MAP.md)** y el script unificado **[`scripts/verify_repo.py`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/scripts/verify_repo.py)**. `REPO_MAP.md` eliminó los paseos erráticos por el árbol de directorios al concentrar en una sola página todos los puntos de entrada, tests y archivos protegidos. Por su parte, `verify_repo.py` sustituyó la incertidumbre de correr múltiples comandos manuales por una única verificación reproducible que ejecuta tests, compilación estática y validación de contrato.

### 4. ¿Qué información pertenece en AGENTS.md y qué información NO debería vivir ahí?
- **Pertenece en `AGENTS.md`**: Orden estricto de lectura (*Read First*), fuentes de verdad canónicas (*Sources of Truth*), comandos estándar (Install, Run, Test, Lint, Verify), límites de cambio (*Change Rules*), condiciones de parada (*Stop Conditions*), directivas de entorno (preservar CRLF, no comandos git) y la Definición de Terminado (*Definition of Done*).
- **NO debe vivir en `AGENTS.md`**: Requerimientos funcionales/no funcionales detallados (viven en `REQUIREMENTS.md`), especificaciones de comportamiento o modelos de dominio (viven en `SPEC.md`), flujos y diagramas de componentes (viven en `ARCHITECTURE.md`), ni secretos o duplicados de código fuente.

### 5. ¿Qué regla convertiste en software/hook/script en lugar de dejarla como instrucción?
La verificación de **integridad contractual del repositorio**. La directiva pasiva *"asegúrate de que no se modifiquen especificaciones protegidas, que no haya secretos y que los requerimientos sigan cubiertos"* fue transformada en el script ejecutable [`scripts/check_repo_contract.py`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/scripts/check_repo_contract.py). Este validador comprueba de forma determinista 7 guardrails: archivos esenciales, trazabilidad de IDs en `SPEC.md`, comandos estándar en `AGENTS.md`, escáner de patrones de credenciales/tokens, integridad de rutas de `REPO_MAP.md`, no duplicidad en la base de datos semilla y contrato de adaptadores.

### 6. ¿Qué diferencia observaste entre 'más contexto' y 'mejor contexto'?
- **'Más contexto'**: Añadir explicaciones extensas, logs redundantes o duplicar información entre múltiples archivos. Tiende a saturar la ventana de contexto del LLM, incrementa el costo y la latencia, y diluye las instrucciones críticas aumentando la probabilidad de alucinaciones.
- **'Mejor contexto'**: Proveer información modular, concisa y jerarquizada con un solo punto de entrada, enlaces directos a los componentes relevantes, fronteras negativas claras (lo que NO se debe hacer) y herramientas de verificación ejecutables. Permite al modelo actuar con foco y precisión.

### 7. ¿Qué riesgo aparece cuando CLAUDE.md/GEMINI.md/copilot instructions duplican información del proyecto?
Se introduce el riesgo de **divergencia y desincronización ("split-brain")**. Cuando se modifica un requerimiento, comando o convención en el proyecto pero no se actualizan todos los archivos de instrucciones de los distintos proveedores de IA, cada agente operará con supuestos contradictorios, violando el principio de *Single Source of Truth* (SSoT). La arquitectura de adaptadores adoptada resuelve esto haciendo que `GEMINI.md` y `CLAUDE.md` deleguen explícitamente en `AGENTS.md`.

### 8. ¿Qué checks comparten ahora el agente, el desarrollador humano y CI?
Comparten exactamente el mismo comando y contrato:
```bash
python scripts/verify_repo.py
```
Que valida de forma secuencial:
1. Pruebas unitarias, de integración, de NFRs y de guardrails (`pytest -q` con 77 pruebas).
2. Verificación de sintaxis y compilación (`python -m compileall -q src test scripts`).
3. Comprobación automática de contrato y políticas del repositorio (`python scripts/check_repo_contract.py`).

### 9. ¿Qué parte del proceso sigue requiriendo decisión humana?
El juicio ético, estratégico y de negocio:
- Priorización y redacción de nuevos requerimientos de usuario.
- Aprobación de cambios en los límites de la arquitectura o tecnologías de persistencia.
- Resolución de conflictos cuando dos requerimientos de negocio colisionan.
- Clasificación de seguridad sobre datos sensibles.
- Autorización final de merge y liberación a producción (*Human in the Loop*).

### 10. ¿Qué evidencia demuestra que el AFTER es realmente mejor?
La evidencia objetiva y medible:
- **0 preguntas de aclaración** solicitadas por el agente.
- **0 comandos fallidos** (frente a 3 en el BEFORE).
- **0 suposiciones incorrectas** (frente a 3 en el BEFORE).
- **0 archivos fuera de alcance modificados**.
- **77/77 pruebas automáticas aprobadas** en ~0.21s con cero regresiones.
- **7/7 guardrails deterministas aprobados** en `check_repo_contract.py`.
- **Salto de puntuación de 59.0 / 100 a 100.0 / 100 (+41.0 puntos)** bajo la rúbrica oficial de madurez.

### 11. ¿Qué mejora realizada para el agente también beneficia a un desarrollador que entra por primera vez al proyecto?
[`docs/REPO_MAP.md`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/docs/REPO_MAP.md) y [`scripts/verify_repo.py`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/scripts/verify_repo.py). Cualquier desarrollador nuevo comprende en 2 minutos la estructura del repositorio, ubica los módulos sin preguntar a un compañero y sabe exactamente cómo verificar su código de forma inequívoca con un solo comando.

### 12. ¿Qué variable no controlada podría afectar tu comparación BEFORE/AFTER?
- La variabilidad estocástica del LLM (muestreo probabilístico, temperatura).
- El estado de la memoria caché del entorno (`.pytest_cache`, `.pyc`).
- Posibles pistas implícitas en el prompt de la segunda ejecución si no se cuida el aislamiento del contexto comparativo.

### 13. ¿Qué elementos de este ADA conservarás como base para tu proyecto final?
1. La estructura central de [`AGENTS.md`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/AGENTS.md) con sus secciones obligatorias (*Sources of Truth*, *Standard Commands*, *Change Rules*, *Stop Conditions* y DoD).
2. El índice de navegación [`docs/REPO_MAP.md`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/docs/REPO_MAP.md) con definición de límites negativos (*Do Not Edit Directly*).
3. El script de validación unificada [`scripts/verify_repo.py`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/scripts/verify_repo.py).
4. El enfoque de **convertir reglas en software** mediante guardrails ejecutables como [`scripts/check_repo_contract.py`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/scripts/check_repo_contract.py).
5. La delegación limpia de adaptadores de agente sin duplicar información.
