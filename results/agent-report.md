# Agent Report
## Agent / Version
Antigravity CLI
## Initial Context 
We are implementing the Customer Search feature.
Before changing code:
1. Read REQUIREMENTS.md.
2. Read SPEC.md.
3. Read ARCHITECTURE.md.
4. Read TASKS.md.
5. Read AGENTS.md.
6. Inspect the current repository.
7. Identify the next incomplete task.
8. Propose the implementation approach.
9. Implement only that task.
10. Run relevant tests.
11. Report changes, verification, and unresolved issues.
Do not invent business requirements.
Do not modify REQUIREMENTS.md or SPEC.md to accommodate an implementation.
## Task Sequence
### T-01
What the agent did:
- Creó la base de datos simulada en memoria en customers.json con 52 registros únicos.
- Incluyó los registros semilla requeridos para los criterios de aceptación de SPEC.md: "Carlos Santana", "Ana Martínez", "José Gómez", "soporte.ti@empresa.com", "Ana", "Anabel" y "Mariana".
- Garantizó que ningún correo electrónico estuviera duplicado.
Human review:
- Se realizó la revisión del json creado.
Tests:
- test_customers_json_exists_and_is_valid: Valida la existencia del archivo y que sea una lista JSON válida.
- test_customers_count_at_least_50: Comprueba que contenga al menos 50 clientes (52 en total).
- test_no_duplicate_emails: Comprueba que el 100% de los correos sean únicos.
- test_acceptance_criteria_seed_records_exist: Verifica la presencia exacta de los clientes necesarios para AC-01, AC-02, AC-04 y AC-06.

### T-02
What the agent did:
- Implementó la clase de dominio Customer en customer.py.
- Dotó a la entidad de los atributos id, nombre y email, agregando la propiedad alias name (getter y setter).
- Implementó un constructor flexible que soporta tanto el orden (id, nombre, email) de SPEC.md como (id, email, nombre) de TASKS.md y argumentos nombrados (name=...).
- Agregó métodos de serialización to_dict(), from_dict(), igualdad estructural (__eq__) y representación (__repr__).
Human review: Revisión de los artefactos creados. COnfirmación de la estructura.
Tests: 
- test_customer_creation_with_attributes: Inicialización estándar con atributos requeridos.
- test_customer_creation_with_email_and_nombre_order: Compatibilidad con orden de parámetros de TASKS.md.
- test_customer_creation_with_nombre_and_email_order: Compatibilidad con orden de parámetros de SPEC.md.
- test_customer_creation_with_name_keyword: Instanciación mediante keyword argument name.
- test_customer_name_setter: Modificación del nombre a través del setter name.
- test_customer_to_dict: Serialización correcta a diccionario.
- test_customer_equality: Comparación por valor entre instancias.
- test_customer_repr: Formato de representación en string.
### T-03
What the agent did:
- Creó el servicio CustomerSearchService en search_services.py.
- Implementó la normalización de texto normalize_text() con descomposición Unicode NFD para eliminar acentos y diéresis de forma insensible a mayúsculas/minúsculas.
- Implementó búsqueda por subcadena en nombre y coincidencia parcial en email con mínimo 3 caracteres.
- Construyó el algoritmo de ordenamiento por relevancia estricta: Coincidencia exacta en nombre > exacta en correo > prefijo en nombre > prefijo en correo > subcadena en nombre > subcadena en correo > desempate alfabético A-Z.
- Añadió respuesta HTTP 404 con el mensaje exacto "No se encontraron clientes para '{término_ingresado}'" (FR-03).
Human review: Revisión de artefactos creados. No estaba incluyendo los NFR.
Tests:
- test_normalize_text: Normalización de acentos, diéresis y mayúsculas.
- test_ac01_substring_and_case_insensitive_matching: Búsqueda de "arl" o "CARLOS" retornando "Carlos Santana".
- test_ac02_accent_normalization: Búsqueda de "jose gomez" retornando "José Gómez".
- test_ac04_email_partial_match: Búsqueda de "sop" o "emp" retornando "soporte.ti@empresa.com".
- test_ac05_only_authorized_basic_fields_returned: Ausencia total de password_hash o tax_id en el DTO de respuesta.
- test_ac06_strict_relevance_ordering: Orden estricto "Ana" > "Anabel" > "Mariana".
- test_fr03_no_results_returns_exact_message: Código 404 y texto exacto cuando no hay resultados.
- test_edge_case_empty_or_whitespace_query: Rechazo con código 400 ante consultas vacías o de sólo espacios.
- test_pagination_limits_to_20_by_default: Validación del límite de 20 registros.
### T-04
What the agent did:
- Creó la jerarquía de excepciones en exceptions.py: CustomerSearchException, EmptyQueryError (400), ValidationError (400), CustomerNotFoundError (404), y DatabaseError (500).
- - Implementó la capa de persistencia CustomerRepository en customer_repository.py para encapsular la lectura de la base de datos y lanzar DatabaseError ante archivos inexistentes o JSON corrupto.
- Implementó la capa Handler CustomerSearchHandler en handler.py según ARCHITECTURE.md.
- Desacopló el servicio para lanzar excepciones de dominio en search_customers() y atraparlas en search() retornando códigos HTTP estandarizados (200, 400, 404, 500).
Human review: Revisión de los artefactos y respuestas.
Tests:
- test_empty_query_error_raised: Lanzamiento explícito de EmptyQueryError.
 - test_empty_query_response_code_400: Mapeo de query vacía a código HTTP 400.
- test_short_query_validation_error: Lanzamiento de ValidationError si longitud < 3 caracteres.
- test_customer_not_found_error_raised: Lanzamiento explícito de CustomerNotFoundError.
- test_customer_not_found_response_code_404: Mapeo a HTTP 404 con texto exacto de FR-03._
- test_database_error_when_file_not_found: Lanzamiento de DatabaseError ante archivo faltante.
- test_database_error_when_file_corrupted: Lanzamiento de DatabaseError ante JSON sintácticamente corrupto.
- test_handler_catches_database_error_and_returns_500: Captura de fallo de persistencia y respuesta HTTP 500 "Error interno del servidor".
- test_handler_successful_search_returns_200: Flujo exitoso a través del Handler retornando HTTP 200.
### T-05
What the agent did: 
- Consolidó y amplió la suite test_search_service.py añadiendo 7 pruebas especializadas de casos borde, desempate alfabético, simetría y contratos de interfaz.
Human review: revisión de los resultados de las pruebas.
Tests:
- test_edge_case_case_insensitivity_symmetry: Valida que "carlos", "Carlos" y "CARLOS" produzcan exactamente la misma lista de resultados.
- test_search_rules_alphabetical_tie_breaker: Comprueba ordenamiento alfabético A-Z entre registros con la misma prioridad de coincidencia.
- test_architecture_request_interface: Comprueba el contrato de payload {"name": "...", "email": "..."} de ARCHITECTURE.md.
- test_happy_path_exact_match: Localización y retorno del registro exacto.
- test_service_traps_all_exceptions_to_http_codes: Verificación de captura uniforme de excepciones retornando 400, 404 y 500.
### T-06
What the agent did: 
- Redactó la documentación integral en README.md explicando cómo preparar el entorno, cómo ejecutar las pruebas, cómo realizar búsquedas mediante la API/Handler y por CLI, contratos de respuesta JSON, reglas de negocio y diagrama de arquitectura.
- Revisó y aseguró que los docstrings de los archivos Python expliquen qué hace cada clase o función a nivel funcional y no cómo lo hace a bajo nivel.
Human review: revisión del resultado de las pruebas.
Tests: Ejecución integral de pytest -v para garantizar que la documentación y comentarios mantuvieran el 100% de las pruebas pasando.
## Problems Encountered
El agente creó un json con información no requerrida ni especificada. Agregó campos como last_name, second_name, complete_name a pesar de tener name.
Al hacer la task 01 no installó pytest.
Nunca informó sobre la librería faltante.
## Human Interventions
Corrección de alucinaciones como el json con campos extra.
Instalación de librerias necesarias. 
## Requirement / Specification Changes

## Final Verification
Verificación del proyecto entero.
## Lessons Learned
Es necesario revisar cada uno de los artefactos. Se aprendió que el flujo de desarrollo es más fácil de probar y verificar utilizando los archivos md correspondientes. Sin embargo, es necesario ser muy especifico y no permitir que asuma demasiadas cosas.
Es necesario revisar los artefactos de desarrollo para reducir ambiguedades.
