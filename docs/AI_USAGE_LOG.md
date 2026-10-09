# AI Usage & Audit Log

| Entradas | Etapa | Evidencia                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | 
| :---: | :--- |:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| 
| 1 | MCP configuration | Se configuró el servidor `github-readonly` en el cliente MCP asociándolo a un Personal Access Token (PAT) delimitado exclusivamente al repositorio `Torres-David/ADA-05-SPEC-DRIVEN`. Se decidió aplicar el Principio de Mínimo Privilegio: conceder únicamente permisos de lectura (`Contents: Read`, `Issues: Read`, `Pull requests: Read`), rechazar credenciales con permisos globales y filtrar el catálogo de esquemas JSON para bloquear cualquier herramienta mutadora (`create_issue`, `push_files`, `comment_pr`).                                                                                         | 
| 2 | Repository analysis | El agente extrajo el contexto estructural del repositorio mediante `get_file_contents` y `search_code`, identificando la arquitectura en capas (Handler, Service, Domain, Repository), los puntos de entrada (`src/cli.py`, `src/handler.py`) y las restricciones no funcionales (latencia $\le$ 300 ms y rate limiting de 30 req/min). Validé este entendimiento contrastando las especificaciones (`REQUIREMENTS.md`, `SPEC.md`, `ARCHITECTURE.md`, `TASKS.md`) y ejecutando la suite automatizada de pruebas `pytest`.                                                                                            | 
| 3 | Issue / PR analysis | La IA inspeccionó el Issue #1 y el PR #2 (rama `Cambio-ADA-06`), detectando que el título usaba el término ambiguo "filtro" en lugar de "ordenamiento", que el issue no contenía descripción en GitHub y que el error HTTP 429 en `handler.py` omitía el campo `"order"`. Verifiqué los resultados y rechacé una inversión global ciega de la lista para no romper la prioridad de relevancia de `AC-06`, y validé manualmente la ejecución de la CLI (`--order asc/desc`) y los 5 nuevos tests unitarios en `test_search_service.py`.                                                                               | 
| 4 | Permission/security review | Se evaluó el modelo de defensa en tres capas (Autenticación del usuario, Autorización del token, Exposición de herramientas MCP) y se analizaron vectores de amenaza como prompt injection, fuga de credenciales, sobre-otorgamiento de privilegios y escape entre repositorios. Confirmé el bloqueo absoluto de herramientas de escritura en el servidor MCP, la ausencia de comandos mutadores en el agente y verifiqué que el token estuviera acotado a un único repositorio para neutralizar cualquier acción no autorizada. | 

# Reflexión
1. ¿Qué información obtuvo el agente mediante MCP que normalmente habrías tenido que copiar al prompt?

El agente pudo obtener el contenido de archivos de código fuente, la estructura de directorios, descripciones completas de Issues y los diffs de los Pull Requests.
Sin MCP, habría tenido que buscar esos archivos manualmente en el IDE o yo tuviera que indicarle directamente en el prompt, lo cual consume tiempo y limita el contexto.
2. ¿Cuál es la diferencia entre el GitHub MCP Server y una GitHub Tool?

MCP Server es un protocolo estándar. Actúa como uin intermediario universal. Permite que los agentes descubran y usen capacidades sin exponerse, porque todas las capacidades ya están configuradas.
Una GitHub Tool es una implementación concreta de ese protocolo, que expone un conjunto específico de capacidades y puede ser configurada con permisos granulares.

3. ¿Qué toolset fue necesario para leer código? ¿Cuál para Issues? ¿Cuál para PRs?

Para leer código se utó get_file_contents y search_repositories, para issues get_issue y list_issues, y para PRs get_pull_request y get_pull_request_diff.

4. ¿Qué diferencia existe entre permisos del PAT y herramientas expuestas por MCP?

El PAT define los permisos de acceso a nivel de repositorio, mientras que las herramientas expuestas por MCP determinan qué acciones específicas puede realizar el agente. Es importante destacar que si el PAT tiene un permiso, pero el MCP no expone esa herramienta, entonces no lo podrá hacer.

5. ¿Por qué se usó read-only aunque el agente pudiera ser capaz de proponer cambios?

Por seguridad y prevención de riesgos

6. ¿Qué evidencia comprobó que el MCP estaba realmente conectado?
agy /mcp que nos otorgó la lista de tools

7. ¿Qué información del Issue era un hecho y qué parte fue inferencia del agente?

El titulo del Issue y el contenido del PR son hechos, mientras que la interpretación de que el término "filtro" era ambiguo y la inferencia de que el error HTTP 429 omitía el campo "order" fueron inferencias del agente basadas en su análisis del código y las especificaciones.

9. ¿Qué relación encontraste entre Issue, PR, código y tests?

El Issue describía una implementación que se deseaba, el PR contenia los cambios del código y el test las validaciones.

9. ¿Qué riesgo tiene tratar el contenido de un Issue o PR como instrucciones confiables?

Propmt Injection y contexto erróneo o incompleto. En este caso se estaba usando "filtro" en lugar de "ordenamiento", lo que podría llevar a una implementación incorrecta si se tomara como instrucción confiable.

10. ¿En qué escenario permitirías escritura mediante MCP? ¿Qué acción requeriría aprobación humana?

Se podría usar en acciones de bajo riesgo como escrituras de PR, borradores de documentación. La aprobación humana sería necesaria en acciones que realicen cambios directos al código o a las ramas.

11. ¿Qué cambiarías si el repositorio fuera privado o perteneciera a una organización?

Asegurarse de que el proveedor del agente no utilice código privado de la empresa para entrenar sus modelos y monitorizar qué archivos está leyendo exactamente el servidor MCP para evitar filtraciones accidentales de secretos o credenciales.

12. ¿Qué aporta MCP al ciclo de vida de Ingeniería de Software frente a copiar/pegar contenido en un chat

Aporta autonomía contextual y un bucle de retroalimentación en tiempo real. Al usar MCP, el agente se convierte en un "compañero de equipo" que puede investigar un problema por sí mismo. Si ve un Issue, puede ir autónomamente a leer el archivo de código mencionado, revisar si hay un PR abierto al respecto, e inspeccionar los tests, todo en una sola interacción. Copiar y pegar requiere que el humano actúe como un motor de búsqueda manual.