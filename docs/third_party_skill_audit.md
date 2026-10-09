# Third-Party Skill Pre-Install Audit
Repository: https://github.com/addyosmani/agent-skills
Selected skill: code-review-and-quality

## Purpose
Proveer un marco integral y riguroso de revisión de código multidimensional (*multi-axis code review*) previo al merge de cambios a la rama principal. La Skill evalúa cinco ejes ortogonales de ingeniería (Corrección, Legibilidad/Simplicidad, Arquitectura, Seguridad y Rendimiento), aplicando compuertas de calidad (*quality gates*), un estándar pragmático de salud incremental del código y proponiendo remedios estructurales concretos.

## Trigger / Description
- **Nombre en frontmatter:** `code-review-and-quality`
- **Descripción formal:**
  > `"Conducts multi-axis code review. Use before merging any change. Use when reviewing code written by yourself, another agent, or a human. Use when you need to assess code quality across multiple dimensions before it enters the main branch. Use when asked to review a diff or a pull request, even when the diff is pasted inline."`
- **Tareas que disparan la Skill:**
  - Revisiones previas al merge de cualquier Pull Request o changeset antes de entrar a `main`.
  - Finalización de una funcionalidad (*feature implementation*) o refactorización.
  - Evaluación de código producido por otro modelo o agente de IA.
  - Auditoría post-fix de errores (inspección del parche y del test de regresión).
  - Peticiones explícitas de revisión de diffs, incluyendo fragmentos pegados directamente en la conversación de chat (*inline diffs*).
- **Tareas que quedan fuera de alcance:**
  - Implementación o desarrollo de código y features desde cero.
  - Ejecución de acciones mutadoras en Git / GitHub (no aprueba, no comenta en remoto ni hace merge).
  - Eliminación silenciosa o no autorizada de código muerto (debe listar y consultar al humano).
  - Modificación o regeneración manual de archivos de bloqueo de dependencias (*lockfiles*).
  - Fases tempranas de ideación de producto, diseño de negocio o especificación inicial.

## Supporting References
- **Archivos auxiliares referenciados internamente:**
  - `../../references/security-checklist.md` (L-353: guía detallada para chequeos exhaustivos de seguridad).
  - `../../references/performance-checklist.md` (L-354: lista de verificación para auditoría de rendimiento).
- **Composición con otras Skills:**
  - [`security-and-hardening`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/.agents/skills/security-and-hardening/SKILL.md) (delegación de análisis profundo de vulnerabilidades y supply chain de librerías).
  - [`performance-optimization`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/.agents/skills/performance-optimization/SKILL.md) (delegación de profiling y optimizaciones críticas).
  - [`constraint-driven-development`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/.agents/skills/constraint-driven-development/SKILL.md) (gestión de umbrales de cobertura y mutation score).

## Tools / Commands / Permissions
- **Scripts y ejecutables:** Ninguno. La Skill carece de scripts autónomos (`.sh`, `.py`, `.ps1`, `.bat`) o binarios.
- **Comandos sugeridos (pasivos):**
  - `npm audit` (mencionado como verificación pasiva de librerías).
  - Ejecución del test runner del proyecto (`pytest`, `npm test`) para validar antes y después.
  - Prueba de mutación experimental manual (inversión temporal de condiciones lógicas para validar que la suite atrape regresiones).
- **Herramientas y permisos requeridos:**
  - Requiere únicamente herramientas de **solo lectura (read-only)** sobre el sistema de archivos local o APIs de repositorios (e.g. `github-readonly`).
  - No requiere permisos de escritura en GitHub, acceso a red externa no controlada, ni elevación de privilegios de administrador del sistema operativo.

## Potential Risks
- **Riesgo de Perfeccionismo Paralizante:** Si el revisor ignora el estándar de aprobación (*"Approve when it definitely improves code health, even if not perfect"*), podría bloquear cambios válidos por discrepancias estilísticas menores.
- **Riesgo de Dependencias Huérfanas de Referencia:** Si las rutas relativas `../../references/security-checklist.md` no existen en el entorno destino, el agente debe apoyarse en sus heurísticas integradas en lugar de fallar.
- **Mitigación de Sesgos (*Sycophancy*):** La Skill aborda activamente este riesgo incorporando una sección obligatoria de "Honesty in Review" que prohíbe el *rubber-stamping* ("LGTM" sin evidencia) y prohíbe suavizar defectos críticos.

## Decision
[X] Install  
[ ] Do not install  

**Reason:**  
La Skill es 100% declarativa y segura: no introduce código ejecutable, dependencias de runtime ocultas ni vectores de inyección. Su huella criptográfica se encuentra anclada (`SHA-256: 2DB1E8...`), opera bajo el principio de mínimo privilegio en solo lectura, y su marco de cinco ejes aporta un estándar de excelencia técnica indispensable para elevar la calidad y mantenibilidad del software sin comprometer la seguridad de la cadena de suministro.
