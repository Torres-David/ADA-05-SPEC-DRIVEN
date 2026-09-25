import json
import os
from typing import List, Optional

try:
    from src.customer import Customer
    from src.exceptions import DatabaseError
except ModuleNotFoundError:
    from customer import Customer
    from exceptions import DatabaseError

DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), "customers.json")
if not os.path.exists(DEFAULT_DB_PATH):
    root_candidate = os.path.join(os.path.dirname(os.path.dirname(__file__)), "customers.json")
    if os.path.exists(root_candidate):
        DEFAULT_DB_PATH = root_candidate


class CustomerRepository:
    """Capa de repositorio para el acceso a la persistencia simulada de clientes."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or DEFAULT_DB_PATH

    def get_all(self) -> List[Customer]:
        """Obtiene todos los clientes desde la persistencia JSON.

        Lanza DatabaseError si el archivo no existe o contiene datos corruptos.
        """
        if not os.path.exists(self.db_path):
            raise DatabaseError(
                f"Base de datos no encontrada en: {self.db_path}"
            )

        try:
            with open(self.db_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                raise DatabaseError("El formato de la base de datos debe ser una lista JSON")

            customers: List[Customer] = []
            for index, item in enumerate(data, start=1):
                cust_id = str(item.get("id", index))
                name = item.get("name") or item.get("nombre", "")
                email = item.get("email", "")
                customers.append(Customer(id=cust_id, nombre=name, email=email))

            return customers
        except (json.JSONDecodeError, OSError) as error:
            raise DatabaseError(f"Fallo al leer la base de datos: {error}") from error
