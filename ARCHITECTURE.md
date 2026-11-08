# Architecture
## Overview
Arquitectura en capas.
## Components
Handler.
Services
Domain
Repository
## Responsibilities
Handler: Recibe la petición HTTP, procesa el payload y lo inyecta a services.
Services: Maneja las reglas de negocio. Hace la petición correspondiente a la base de datos, pero se encarga de empaquetar la respuesta según corresponda. Realiza validaciones de regla de negocio como ordenamiento.
Domain: Modelos y estructuras necesarias.
Repository: Contacto con la persistencia.
## Data Flow
La información llega a el Handler, procesa la solicitud e inyecta datos al servicio. El servicio realiza las reglas de negocio y si es necesario se contacta con la capa repository para las solicitudes. La respuesta de repository se pasa a services y services crea el DTO para la respuesta. Service devuelve el DTO y handler responde.
## Interfaces
Request:
{
"email" : "ejemplo@gmail.com",
"name": "david torres"
}
## Error Handling
Errores internos respuesta 500
No encontrado 404
encontrado correctamente 200
## Testing Strategy
Se realizaran test unitarios y de integracion.
## Dependencies
N/A
## Design Decisions
Se decidio esta arquitectura para facilitar el principio de una sola responsabilidad, la revision  y mantenibilidad del codigo.
## Trade-offs
Esta arquitectura facilita el entendimiento del codigo, sin embargo genera muchos archivos para una funcionalidad sencilla.