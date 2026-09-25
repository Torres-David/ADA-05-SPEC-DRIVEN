import threading
import time
from typing import Any, Dict, List, Optional

from exceptions import RateLimitExceededError
from search_services import CustomerSearchService


class RateLimiter:
    """Controlador de límite de tasa en memoria basado en ventana deslizante de 60 segundos."""

    def __init__(self, max_requests: int = 30, window_seconds: float = 60.0):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._user_requests: Dict[str, List[float]] = {}
        self._lock = threading.Lock()

    def check_and_record(self, user_id: str) -> bool:
        """Verifica si el usuario puede realizar la petición y registra la marca de tiempo.

        Retorna True si la petición es permitida, False si supera la cuota permitida.
        """
        now = time.time()
        with self._lock:
            timestamps = self._user_requests.get(user_id, [])
            # Filtrar registros dentro de la ventana de tiempo (60s)
            valid_timestamps = [t for t in timestamps if now - t < self.window_seconds]

            if len(valid_timestamps) >= self.max_requests:
                self._user_requests[user_id] = valid_timestamps
                return False

            valid_timestamps.append(now)
            self._user_requests[user_id] = valid_timestamps
            return True

    def reset(self, user_id: Optional[str] = None) -> None:
        """Reinicia el contador de peticiones para un usuario o para todos."""
        with self._lock:
            if user_id:
                self._user_requests.pop(user_id, None)
            else:
                self._user_requests.clear()


class CustomerSearchHandler:
    """Capa Handler según ARCHITECTURE.md y requisitos no funcionales.

    Recibe la petición HTTP/payload, aplica rate limiting por usuario autenticado (NFR-02)
    e inyecta la solicitud al servicio de búsqueda devolviendo la respuesta correspondiente.
    """

    def __init__(
        self,
        service: Optional[CustomerSearchService] = None,
        rate_limiter: Optional[RateLimiter] = None,
        enable_rate_limit: bool = True,
    ):
        self.service = service or CustomerSearchService()
        self.rate_limiter = rate_limiter or RateLimiter(max_requests=30, window_seconds=60.0)
        self.enable_rate_limit = enable_rate_limit

    def handle(
        self,
        request_payload: Any,
        page: int = 1,
        limit: int = 20,
        user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Procesa la petición y retorna la respuesta con su código de estado HTTP correspondiente:

        - 200: Encontrado correctamente.
        - 400: Petición inválida o vacía.
        - 404: No encontrado (con mensaje de negocio exacto).
        - 429: Too Many Requests (límite de 30 req/min por usuario superado - NFR-02).
        - 500: Error interno de servidor o base de datos.
        """
        # Identificar usuario autenticado para NFR-02
        resolved_user_id = user_id
        if resolved_user_id is None and isinstance(request_payload, dict):
            resolved_user_id = (
                request_payload.get("user_id")
                or request_payload.get("authenticated_user")
                or request_payload.get("user")
            )

        resolved_user_id = str(resolved_user_id) if resolved_user_id is not None else "default_user"

        # Aplicar Rate Limiting (NFR-02)
        if self.enable_rate_limit:
            if not self.rate_limiter.check_and_record(resolved_user_id):
                error = RateLimitExceededError()
                return {
                    "status": error.status_code,
                    "message": error.message,
                    "data": [],
                }

        return self.service.search(request_payload, page=page, limit=limit)
