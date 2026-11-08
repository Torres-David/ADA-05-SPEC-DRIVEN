# Human Review Decisions

## Change
CR-02

### RF-01
Reviewer severity: SHOULD FIX
Human decision: ACCEPTED
Reason: El hallazgo está técnicamente sustentado por SPEC.md (línea 37: "Invalid formats raise ValidationError (HTTP 400)"). Proporcionar un dominio malformado con múltiples `@` (ej. `"@@empresa.com"`) o una dirección de correo completa (ej. `"user@empresa.com"`) no debe derivar en un HTTP 404 (cliente no encontrado), sino en un HTTP 400 Bad Request por formato de dominio inválido.
Required action: En `src/search_services.py`, actualizar la normalización y validación de `email_domain` para remover todos los `@` al inicio (`.lstrip("@")`) y verificar que no existan caracteres `@` adicionales dentro del dominio (`"@" in stripped_domain`). Agregar pruebas unitarias en `test/test_search_service.py` que comprueben que `"user@empresa.com"` y `"@@empresa.com"` lanzan `ValidationError` (HTTP 400).

### RF-02
Reviewer severity: SHOULD FIX
Human decision: MODIFIED
Reason: El problema de cobertura es real, pero crear un arnés complejo de pruebas de integración por procesos para `main()` de `src/cli.py` excede el alcance directo de CR-02, dado que `CustomerSearchHandler` ya está 100% probado. La severidad se mantiene pero se acota la solución a la verificación unitaria directa de la función de formateo `format_search_results` y el parsing de argumentos.
Final severity: SHOULD FIX
Required action: Agregar pruebas unitarias focalizadas en `test/test_search_service.py` o un archivo de pruebas complementario que comprueben que `format_search_results` renderiza correctamente el sufijo `", Dominio @empresa.com"` en el estado HTTP 200 y omite el sufijo cuando `email_domain` es `None`.

### RF-03
Reviewer severity: OPTIONAL
Human decision: DEFERRED
Reason: Las 4 líneas de normalización en el manejador de `CustomerNotFoundError` de `search()` funcionan adecuadamente y están localizadas dentro del mismo archivo `src/search_services.py`. No introduce defectos de ejecución en producción.
Required action: Registrar como deuda técnica menor en el backlog para una posterior refactorización de limpieza de servicios; no bloquea la aprobación de CR-02.

### RF-04
Reviewer severity: OPTIONAL
Human decision: REJECTED
Reason: La especificación y el Change Request CR-02 delimitan el alcance al parámetro opcional de búsqueda, la bandera CLI `--email-domain` y el soporte vía payload/kwargs. El bucle interactivo de terminal (`while True:`) es una utilidad complementaria previa y la interacción por consola no fue solicitada en los requisitos ni criterios de aceptación de CR-02.
Required action: Ninguna. Mantener el modo interactivo actual sin modificaciones.

## Human Gate
[x] Return to coder-agent
[ ] Ready for final re-review
[ ] Stop / escalate
