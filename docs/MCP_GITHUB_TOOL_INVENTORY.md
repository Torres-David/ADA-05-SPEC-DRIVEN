# Inventario de Herramientas GitHub MCP (`github-readonly`)


| Tool / Capacidad | Toolset | Read/Write | Uso en el ADA | Riesgo |
| :--- | :--- | :--- | :--- | :--- |
| `get_file_contents` / lectura de archivos | `repos` | Read | Leer código fuente, configuraciones y documentación del repositorio remoto | **Bajo**: Solo lectura de contenido de archivos. |
| `search` (`search_code`, `search_repositories`) / búsqueda | `repos` | Read | Localizar implementaciones, referencias de símbolos o repositorios relacionados | **Bajo**: Consulta de índices públicos o autorizados. |
| `list_directory` / navegación de árbol de archivos | `repos` | Read | Inspeccionar estructura de carpetas y jerarquía de directorios remotos | **Bajo**: Solo metadatos y listado de rutas. |
| `issue_read` (`get_issue`, `list_issues`) / lectura de Issues | `issues` | Read | Comprender requerimientos, reportes de bugs y solicitudes de usuarios | **Medio**: Contenido no confiable (posible vector de *prompt injection* indirecto en descripciones/comentarios). |
| `issue_comments_read` (`list_issue_comments`) / comentarios de Issue | `issues` | Read | Analizar discusiones técnicas y contexto adicional de incidencias | **Medio**: Contenido no confiable generado por usuarios externos. |
| `pull_request_read` (`get_pull_request`, `list_pull_requests`) / lectura de PR | `pull_requests` | Read | Analizar contexto de cambios, diffs, ramas y metadatos de integración | **Medio**: Contenido no confiable en títulos, descripciones o revisiones externas. |
| `pull_request_files` (`list_pull_request_files`) / archivos de PR | `pull_requests` | Read | Revisar la lista de archivos modificados en un Pull Request | **Bajo**: Listado estructural de rutas modificadas. |
| **Write tools** (`create_or_update_file`, `push_files`, `create_issue`, `create_pull_request`, `merge_pull_request`, etc.) | — | **No disponibles** | Bloqueadas explícitamente por política `X-MCP-Readonly: true` y filtrado de toolsets | **Alto si estuvieran habilitadas**: Riesgo de alteración no controlada de ramas, commits no autorizados o cierre indebido de PRs/Issues. |
