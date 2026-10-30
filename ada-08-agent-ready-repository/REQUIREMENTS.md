# Requirements — Customer Search
## User Story
As a user,
I want to search customers by name or email,
so that I can quickly find the customer record I need.
## Functional Requirements
FR-01: The system must return records where the search string matches as a substring within the `first_name` or `last_name` fields, in a case-insensitive manner.
FR-02:The search engine must normalize accents, diaereses, and special characters when comparing text.
FR-03: Si la búsqueda no arroja coincidencias en la base de datos, la 
interfaz debe mostrar exactamente el texto: "No se encontraron 
clientes para '{término_ingresado}'".
FR-04: The system must return records where the entered text partially matches the customer's email field. The system considers it a partial match if there are 3 matching characters in the same order.
FR-05:The system must only return basic customer information. Information classified as sensitive must not be allowed to reach the public-facing front end.
FR-06:Se debe poder realizar búsquedas por medio de correo electrónico
## Non-Functional Requirements
NFR-01:The 95th percentile (p95) of the search endpoint response time must be less than or equal to 300 ms under a sustained load of 50 concurrent requests per second.
NFR-02: The system must apply rate limiting of a maximum of 30 search requests per minute per authenticated user. Upon exceeding the limit, the API must reject requests with the HTTP code 429 Too Many Requests.
NFR-03: The search component must comply with the WCAG 2.1 Level AA standard, allowing for full keyboard navigation (Tab, Enter, and arrow keys) and maintaining a minimum text-to-background contrast ratio of 4.5:1.
## Open Questions
Q-01:
Q-02:
## Constraints / Assumptions
C-01:
A-01:
