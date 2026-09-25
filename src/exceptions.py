class CustomerSearchException(Exception):
    """Excepción base para el módulo de búsqueda de clientes."""

    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class EmptyQueryError(CustomerSearchException):
    """Lanzada cuando el término o query de búsqueda está vacío o contiene sólo espacios."""

    def __init__(self, message: str = "El término de búsqueda no puede estar vacío"):
        super().__init__(message, status_code=400)


class ValidationError(CustomerSearchException):
    """Lanzada cuando la petición o término no cumple con las validaciones de negocio."""

    def __init__(self, message: str = "Parámetros de búsqueda inválidos"):
        super().__init__(message, status_code=400)


class CustomerNotFoundError(CustomerSearchException):
    """Lanzada cuando no se encuentran registros en la búsqueda (FR-03)."""

    def __init__(self, term: str):
        message = f"No se encontraron clientes para '{term}'"
        super().__init__(message, status_code=404)
        self.term = term


class DatabaseError(CustomerSearchException):
    """Lanzada cuando ocurre un error en la persistencia o base de datos simulada."""

    def __init__(self, message: str = "Error interno de base de datos"):
        super().__init__(message, status_code=500)


class RateLimitExceededError(CustomerSearchException):
    """Lanzada cuando se supera el límite de 30 peticiones por minuto por usuario (NFR-02)."""

    def __init__(
        self,
        message: str = "Too Many Requests: Se ha excedido el límite de 30 peticiones por minuto por usuario",
    ):
        super().__init__(message, status_code=429)
