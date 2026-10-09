# AI Usage & Audit Log

| Entradas | Etapa | Evidencia                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | 
| :---: | :--- |:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| 
| 1 | Workflow observation | En cuestión del workflow, lo desarrolló correctamente. Sin embargo, en los artefactos resultantes estaba incluyendo generar siempre un workflow_observation.md, además de siempre editar este AI_USAGE_LOG.md, solo porque lo vio en el proyecto. Estas decisiones innecesarias se rechazaron.                                                                                                                                                                                                                                   | 
| 2 | Skill authoring  | Se realizaron cambios en el alcance. Durante las pruebas se observó que el agente decidió explorar todo el proyecto, revisar cambios locales no commiteados, e hizo una exploración de archivos innecesaria. Se actualizó el flujo para limitarlo exclusivamente a las especificaciones del skill.                                                                                                                                                                                                                               | 
| 3 | Script/reference design  | Se retiró la información especifica para hacer que apunte a las referencias.                                                                                                                                                                                                                                                                                                                                                                                                                                                     | 
| 4 | Permission/security review | Se evaluó el modelo de defensa en tres capas (Autenticación del usuario, Autorización del token, Exposición de herramientas MCP) y se analizaron vectores de amenaza como prompt injection, fuga de credenciales, sobre-otorgamiento de privilegios y escape entre repositorios. Confirmé el bloqueo absoluto de herramientas de escritura en el servidor MCP, la ausencia de comandos mutadores en el agente y verifiqué que el token estuviera acotado a un único repositorio para neutralizar cualquier acción no autorizada. | 

# Reflexión

1. ¿Qué parte del workflow pertenece al juicio del LLM y cuál debe ser determinista?

Los requerimientos, la arquitectura y las tareas deben ser deterministas. Las revisiones de cómo se va a afectar el código y permisos siempre se deben revisar por humanos. El juicio del LLM es más útil para la generación de prompts, la revisión de artefactos y la generación de tests.
2. ¿Qué información moviste de SKILL.md a references/ y por qué?

El workflow, para evitar que el SKILL se "ensucie".

3. ¿Qué función cumple la description del frontmatter en el routing?
Funciona como contrato entre la instrucción y la Skill.

4. ¿Qué prompt negativo fue más difícil de evitar que activara la Skill?

  El prompt negativo más desafiante fue "Merge PR #04." (y su variante híbrida en casos de borde: "Review PR #04 and merge it if everything looks good").
 Sin fronteras negativas explícitas, el LLM asume intuitivamente que la revisión es un paso previo que habilita la ejecución del merge.

5. ¿Qué diferencia práctica observaste entre una Skill y un MCP Server?

Expone funciones, simplemente ejecuta llamadas técnica. En cambio una skill tiene un flujo de trabajo detallado. Enseña qué debe hacer y cómo debe hacerlo.

6. ¿Qué aporta el script que no conviene resolver con instrucciones de lenguaje natural?

aporta determinismo estricto e infalibilidad sintáctica, algo que el lenguaje natural no puede garantizar.

7. ¿Qué riesgo existiría si esta Skill pudiera comentar o hacer merge en GitHub?

Habría riesgo de que la Skill haga cambios no autorizados en el repositorio, lo que podría comprometer la integridad del código y la seguridad del proyecto. Además, podría introducir errores o vulnerabilidades sin revisión humana, afectando la calidad del software y la confianza en el sistema de control de versiones.
De hecho, aumenta el riesgo de que el agente manipule el código para cumplir con sus propios objetivos, en lugar de seguir las intenciones del equipo de desarrollo.

8. ¿Qué cambió entre la primera y la última versión de tu Skill?

El mayor cambio fue el alcance, para evitar desviaciones innecesarias y centrarse exclusivamente en las especificaciones del skill. Se eliminaron exploraciones de archivos no relevantes y se ajustaron los prompts para que fueran más específicos y alineados con los objetivos del proyecto.

9. ¿Qué evidencia te permite afirmar que la Skill es reutilizable?

El uso de plantillas reutilizables y que la SKILL no tiene rutas redirigdas directamente al repositorio, sino que funciona por número de referencia.

10. ¿Qué otro proceso profesional de Ingeniería de Software convertirías en una Skill?

Migración de base de datos y refactorización de código.

11. ¿Qué diferencia de diseño fue más evidente entre tu Skill y code-review-and-quality?

Nosotro priorizamos trazabilidad, el profesional la calidad.

12. ¿Qué ventaja y qué costo observaste al usar una Skill mucho más extensa y opinionated?

Ventaja:
- Diagnosticó hallazgos que pasaron desapercibidos en revisiones convencionales.
Costo:
- Sobrecarga de Contexto y Latencia: Cargar un archivo SKILL.md de 399 líneas consume miles de tokens.

13. ¿Qué controles aplicarías antes de adoptar una Skill de terceros en un repositorio empresarial?

 Aplicaría la matriz de Supply Chain Hygiene verificada en este ADA.

14. Después de estudiar la Skill profesional, ¿qué cambiarías en una versión 2 de tu Skill y cómo evaluarías que
realmente mejoró?

Pruebas de Mutación Experimental en Verificación: Incorporar al workflow la técnica de mutar temporalmente una condición lógica en el código para verificar empíricamente que los tests fallen (confirmando que no haya pruebas en falso verde).
