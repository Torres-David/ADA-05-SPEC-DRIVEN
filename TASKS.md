# Tasks
## T-01 Project setup
- Goal: Crear el entorno del proyecto. Desarrollar una base de datos simulada, en memoria.
- Files: JSON de la información de los clientes. 
- Acceptance: El JSON que funcionará como base de datos simulada debe incluir al menos 50 clientes.
- Verification: Ningun email debe ser repetido.
## T-02 Domain model
- Goal: Crear la entidad usuario.
- Files: customer.py
- Acceptance: Usuario con id, email y nombre.
- Verification: pytest
## T-03 Search logic
- Goal: Funcionalidad de búsqueda. Incluir validación del json request. Incluir protección de errores y respuesta. Ordenar por medio de los requerimientos.
- Files: search_services.py
- Acceptance: se logra hacer búsquedas dentro del json que simula base de datos en memoria.
- Verification:pytest
## T-04 Validation and errors
- Goal: Excepciones para los errores de la base de datos, respuesta ante solicitud vacía.
- Files: 
- Acceptance: Las excepciones se atrapan y se responde con el codigo http adecuado.
- Verification:pytest
## T-05 Tests
- Goal: Agregar test para los criterios de aceptacion y respuesta a errores.
- Files: test_search_service.py
- Acceptance: El sistema atrapa correctamente los errores
- Verification:pytest
## T-06 Documentation
- Goal: Documentación de cómo correr el programa y cómo realizar busquedas (esto incluirlo en el README.md) y documentacion del código por medio de comentarios que explican qué hace, no como.
- Files: README.md, archivos pyton
- Acceptance: Los archivos se les agrega la documentacion correspondiente.
- Verification: Manual