import unicodedata
from typing import Any, Dict, List, Optional, Tuple

try:
    from src.customer import Customer
    from src.customer_repository import CustomerRepository
    from src.exceptions import (
        CustomerNotFoundError,
        CustomerSearchException,
        DatabaseError,
        EmptyQueryError,
        ValidationError,
    )
except ModuleNotFoundError:
    from customer import Customer
    from customer_repository import CustomerRepository
    from exceptions import (
        CustomerNotFoundError,
        CustomerSearchException,
        DatabaseError,
        EmptyQueryError,
        ValidationError,
    )


def normalize_text(text: str) -> str:
    """Normaliza texto removiendo acentos, diéresis y convirtiendo a minúsculas."""
    if not text:
        return ""
    decomposed = unicodedata.normalize("NFD", text)
    without_accents = "".join(
        char for char in decomposed if unicodedata.category(char) != "Mn"
    )
    return without_accents.lower().strip()


class CustomerSearchService:
    """Servicio que encapsula la lógica de búsqueda y reglas de negocio para clientes."""

    def __init__(
        self,
        db_path: Optional[str] = None,
        customers: Optional[List[Customer]] = None,
        repository: Optional[CustomerRepository] = None,
    ):
        self.repository = repository or CustomerRepository(db_path=db_path)
        self._custom_customers: Optional[List[Customer]] = (
            list(customers) if customers is not None else None
        )

    @property
    def customers(self) -> List[Customer]:
        """Obtiene la lista de clientes en memoria o a través del repositorio."""
        if self._custom_customers is not None:
            return self._custom_customers
        return self.repository.get_all()

    @customers.setter
    def customers(self, value: Optional[List[Customer]]) -> None:
        self._custom_customers = list(value) if value is not None else None

    def _calculate_match_priority(
        self, query: str, customer: Customer
    ) -> Optional[int]:
        """Calcula la prioridad de relevancia de la coincidencia para un cliente.

        Prioridades:
        1: Coincidencia exacta por nombre
        2: Coincidencia exacta por correo
        3: Coincidencia de prefijo por nombre
        4: Coincidencia de prefijo por correo
        5: Coincidencia de subcadena por nombre
        6: Coincidencia de subcadena por correo
        None: No coincide
        """
        norm_name = normalize_text(customer.name)
        norm_email = normalize_text(customer.email)

        # 1. Coincidencia exacta en nombre
        if norm_name == query:
            return 1

        # 2. Coincidencia exacta en correo (o nombre de usuario del correo)
        email_user = norm_email.split("@")[0] if "@" in norm_email else norm_email
        if norm_email == query or email_user == query:
            return 2

        # 3. Coincidencia de prefijo en nombre
        if norm_name.startswith(query):
            return 3

        # 4. Coincidencia de prefijo en correo
        if norm_email.startswith(query):
            return 4

        # 5. Coincidencia de subcadena en nombre
        if query in norm_name:
            return 5

        # 6. Coincidencia de subcadena en correo
        if query in norm_email:
            return 6

        return None

    def search_customers(
        self,
        request_payload: Any,
        page: int = 1,
        limit: int = 20,
        order: str = "asc",
    ) -> Dict[str, Any]:
        """Ejecuta la búsqueda y lanza excepciones de dominio si ocurren validaciones o ausencias."""
        # 1. Extracción del término y orden
        raw_term = ""
        raw_order = order
        if isinstance(request_payload, dict):
            name_term = request_payload.get("name", "")
            email_term = request_payload.get("email", "")
            query_term = request_payload.get("query", "")
            if "order" in request_payload and request_payload["order"] is not None:
                raw_order = request_payload["order"]

            if query_term:
                raw_term = str(query_term)
            elif name_term and email_term:
                raw_term = str(name_term).strip() or str(email_term).strip()
            elif name_term:
                raw_term = str(name_term)
            elif email_term:
                raw_term = str(email_term)
        elif isinstance(request_payload, str):
            raw_term = request_payload
        else:
            raise ValidationError("Formato de solicitud inválido")

        # Validación de parámetro de ordenamiento ('asc' o 'desc')
        clean_order = str(raw_order).lower().strip()
        if clean_order not in ("asc", "desc"):
            raise ValidationError("El parámetro de ordenamiento debe ser 'asc' o 'desc'")

        # Validación de solicitud vacía o solo espacios (Edge case SPEC.md / T-04)
        trimmed_term = raw_term.strip()
        if not trimmed_term:
            raise EmptyQueryError("El término de búsqueda no puede estar vacío")

        # Regla de búsqueda: al menos 3 caracteres consecutivos
        if len(trimmed_term) < 3:
            raise ValidationError("El término de búsqueda debe tener al menos 3 caracteres")

        normalized_query = normalize_text(trimmed_term)

        # 2. Filtrado y ordenamiento por relevancia
        matched_customers: List[Tuple[int, str, Customer]] = []
        for customer in self.customers:
            priority = self._calculate_match_priority(normalized_query, customer)
            if priority is not None:
                matched_customers.append(
                    (priority, normalize_text(customer.name), customer)
                )

        # Ordenar respetando la prioridad de coincidencia y aplicando el criterio alfabético
        if clean_order == "desc":
            matched_customers.sort(key=lambda item: item[1], reverse=True)
            matched_customers.sort(key=lambda item: item[0], reverse=False)
        else:
            matched_customers.sort(key=lambda item: (item[0], item[1]))

        # 3. Verificación de coincidencias (FR-03: lanza CustomerNotFoundError)
        if not matched_customers:
            raise CustomerNotFoundError(trimmed_term)

        # 4. Paginación
        total_records = len(matched_customers)
        safe_limit = max(1, limit)
        safe_page = max(1, page)
        start_index = (safe_page - 1) * safe_limit
        paginated_items = matched_customers[start_index : start_index + safe_limit]

        # 5. Empaquetado DTO con datos básicos autorizados (FR-05, AC-05)
        dto_results = [
            {
                "id": cust.id,
                "name": cust.name,
                "email": cust.email,
            }
            for _, _, cust in paginated_items
        ]

        return {
            "status": 200,
            "message": "Búsqueda exitosa",
            "total": total_records,
            "page": safe_page,
            "limit": safe_limit,
            "order": clean_order,
            "data": dto_results,
        }

    def search(
        self,
        request_payload: Any,
        page: int = 1,
        limit: int = 20,
        order: str = "asc",
    ) -> Dict[str, Any]:
        """Punto de entrada compatible que atrapa excepciones de dominio y empaqueta

        la respuesta con el código HTTP correspondiente.
        """
        try:
            return self.search_customers(
                request_payload, page=page, limit=limit, order=order
            )
        except CustomerNotFoundError as not_found:
            resolved_order = (
                str(order).lower().strip()
                if str(order).lower().strip() in ("asc", "desc")
                else "asc"
            )
            return {
                "status": not_found.status_code,
                "message": not_found.message,
                "total": 0,
                "page": page,
                "limit": limit,
                "order": resolved_order,
                "data": [],
            }
        except DatabaseError as db_error:
            return {
                "status": 500,
                "message": "Error interno del servidor",
                "error": db_error.message,
                "data": [],
            }
        except CustomerSearchException as domain_error:
            return {
                "status": domain_error.status_code,
                "message": domain_error.message,
                "data": [],
            }
        except Exception as error:
            return {
                "status": 500,
                "message": "Error interno del servidor",
                "error": str(error),
                "data": [],
            }
