# AI Usage Log - ADA-09

## Entradas Significativas del Ciclo

### 1. Definición o Refinamiento del Change Request
- Se refinó el requerimiento para incorporar el filtrado opcional por dominio de correo (email_domain), estableciendo la normalización requerida (remoción de arroba inicial y comparación insensible a mayúsculas y minúsculas), la validación de formato (rechazo con HTTP 400 Bad Request) y la preservación del comportamiento previo sin regresiones cuando el parámetro no se proporciona.

### 2. Plan del Coder-Agent y Decisión Humana sobre el Plan
- El plan desglosó la intervención en CustomerSearchService (validación, normalización y filtrado de dominio), CustomerSearchHandler (paso de argumentos opcionales) y cli.py (bandera de línea de comandos y formateo). Validé que no se alteraran las interfaces existentes y que se mantuviera la suite de 77 pruebas previa como compuerta de regresión.

### 3. Implementación: Sugerencia Relevante Aceptada y Rechazada
- Acepté la sugerencia de propagar el parámetro email_domain tanto por diccionario de carga útil (payload) como por argumento nombrado en los métodos principales. Se rechazó modificar directamente el repositorio de persistencia (CustomerRepository) o el archivo JSON de datos, manteniendo el repositorio como almacenamiento de lectura neutro y ubicando toda la regla de negocio y filtrado exclusivamente en la capa de servicios según ARCHITECTURE.md.

### 4. Reviewer-Agent: Finding Relevante y Evidencia
- El reviewer identificó que la validación de formato en search_services.py permitía cadenas con arrobas intermedias (como usuario@empresa.com) o múltiples arrobas iniciales (como @@empresa.com). Al no rechazarse en la validación inicial, el algoritmo de búsqueda no encontraba coincidencias y lanzaba CustomerNotFoundError (HTTP 404) en lugar de ValidationError (HTTP 400), violando la regla de validación de SPEC.md. Se aportó como evidencia el código exacto de la condición y la traza de ejecución que devolvía 404.

### 5. Human Review: Finding Aceptado, Modificado o Rechazado y por qué
- Acepté el hallazgo RF-01 porque SPEC.md exige explícitamente HTTP 400 para formatos inválidos. Modifiqué el hallazgo RF-02 acotando la exigencia de pruebas a la función de formateo de consola format_search_results para no sobrecargar el alcance con pruebas pesadas de subprocesos y rechacé el hallazgo RF-04 (falta de soporte en el bucle interactivo de consola) porque no formaba parte del Change Request.

### 6. Fix y Re-Review: Qué Cambió Después de la Revisión
- En search_services.py se añadió la restricción para descartar cualquier arroba remanente dentro de la cadena del dominio. En cli.py se implementó una importación modular protegida para CustomerSearchHandler, permitiendo probar format_search_results de forma directa. Se agregaron dos pruebas unitarias nuevas alcanzando 86 pruebas en verde, permitiendo al re-reviewer certificar el estado READY FOR HUMAN MERGE sin regresiones.

---

## Reflexión Individual

### 1. ¿Qué encontró el reviewer-agent que el coder-agent no detectó?
El reviewer-agent descubrió un caso límite de validación donde dominios con arroba interna (como usuario@empresa.com) o múltiples arrobas iniciales (como @@empresa.com) pasaban la validación de formato sin disparar ValidationError. Esto provocaba que el sistema buscara en la base de datos y retornara un HTTP 404 (cliente no encontrado) en vez del HTTP 400 (solicitud incorrecta) estipulado por el contrato de especificación.

### 2. ¿Qué finding fue más difícil de clasificar y por qué?
El hallazgo RF-02 respecto a la cobertura de pruebas de la interfaz de línea de comandos. Fue complejo clasificarlo entre SHOULD FIX y OPTIONAL porque la lógica medular del servicio y el manejador ya contaban con pruebas completas, pero el archivo cli.py presentaba cambios en el formateo de salida y en los argumentos sin una sola prueba que protegiera dicha capa contra regresiones visuales.

### 3. ¿Qué finding rechazaste o modificaste como humano y qué evidencia usaste?
Se modificó RF-02 (falta de tests en el CLI), limitando el requerimiento a pruebas unitarias de format_search_results para no exigir un arnés de integración de subprocesos fuera de proporción con el cambio. Se rechazó RF-04 (soporte en el modo interactivo del CLI) usando como evidencia el Change Request CR-02, el cual especifica la bandera por línea de comandos y el payload pero no incluye el bucle interactivo en su alcance ni en sus criterios de aceptación.

### 4. ¿Hubo algún test verde que produjera falsa confianza? Explica.
Sí. La prueba inicial test_email_domain_invalid_format_raises_validation_error verificaba siete casos de dominios inválidos (vacío, espacios, sin punto, puntos en extremos o tipo numérico) y pasaba al 100% en verde. Sin embargo, no incluía entradas con arrobas intermedias ni múltiples arrobas iniciales, lo que generaba una falsa sensación de que cualquier entrada malformada estaba cubierta cuando en realidad se filtraban formatos anómalos que terminaban en respuestas 404.

### 5. ¿Verificaste alguna API o dependencia que parecía plausible? ¿Qué encontraste?
Se verificó si existía alguna librería externa de validación de correos o dominios (como email-validator o validator-collection). Se constató que el repositorio está diseñado para operar con cero dependencias externas fuera de pytest y la biblioteca estándar de Python (re, json, unicodedata, argparse, threading). Cualquier intento de importar paquetes externos hubiera roto el contrato de empaquetado y las directrices de AGENTS.md.

### 6. ¿Qué arquitectura o regla del repositorio fue más útil para la revisión?
La regla de separación de responsabilidades y flujo unidireccional definida en ARCHITECTURE.md (CLI a Handler, Handler a Service, Service a Repository). Esta regla impidió que la lógica de filtrado de dominios se colocara en el Handler o en el CLI, forzando a que toda la validación, normalización y cálculo de coincidencia residiera exclusivamente dentro de CustomerSearchService.

### 7. ¿Qué problema pudo detectar un check determinista antes que el reviewer-agent?
El script check_repo_contract.py detectó inmediatamente la consistencia de los comandos estándar, la integridad del esquema de la base de datos de prueba y la ausencia total de credenciales o secretos en el código fuente. Estas comprobaciones automáticas ahorran tiempo al revisor, quien puede concentrarse plenamente en la semántica del negocio y la lógica de validación.

### 8. ¿Qué parte del review sigue requiriendo criterio humano?
La ponderación del impacto del alcance frente a la deuda técnica. Un agente puede señalar correctamente que falta una prueba o que existe una pequeña duplicación, pero se requiere discernimiento humano para determinar si abordar esa observación beneficia la entrega o introduce una sobreingeniería innecesaria que desvía el objetivo del cambio solicitado.

### 9. ¿Qué technical debt aceptaste o diferiste y por qué?
Se difirió el hallazgo RF-03, que señalaba la duplicación de cuatro líneas de normalización de cadenas de texto entre el método search_customers y el bloque de captura de CustomerNotFoundError en el método search. Se postergó porque el código es breve, totalmente interno a una misma clase, está cubierto por pruebas y no provoca efectos secundarios en tiempo de ejecución.

### 10. ¿Qué artefactos de este ADA reutilizarías en la Agentic Software Factory final?
Reutilizaría cuatro artefactos: el contrato de repositorio automatizado (check_repo_contract.py), el validador estructural de reportes de revisión (validate_review_report.py), la plantilla de trazabilidad integral (PR_EVIDENCE.md) y el formato estructurado de decisiones humanas (human-review-decisions.md). Todos ellos crean barreras deterministas que aseguran rigor sin depender exclusivamente del juicio del modelo de lenguaje.
