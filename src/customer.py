from typing import Any, Dict, Optional


class Customer:
    """Entidad de dominio que representa a un cliente/usuario del sistema."""

    def __init__(
        self,
        id: str = "",
        nombre: Optional[str] = None,
        email: Optional[str] = None,
        name: Optional[str] = None,
    ):
        self.id = str(id) if id is not None else ""

        # Determinación flexible de nombre y email para soportar orden de parámetros
        # según SPEC.md (id, nombre, email) y TASKS.md (id, email, nombre)
        raw_name = nombre if nombre is not None else name
        raw_email = email

        if raw_name is not None and raw_email is not None:
            if "@" in str(raw_name) and "@" not in str(raw_email):
                raw_name, raw_email = raw_email, raw_name

        self.nombre: str = str(raw_name) if raw_name is not None else ""
        self.email: str = str(raw_email) if raw_email is not None else ""

    @property
    def name(self) -> str:
        """Alias para el atributo nombre."""
        return self.nombre

    @name.setter
    def name(self, value: str) -> None:
        self.nombre = str(value) if value is not None else ""

    def to_dict(self) -> Dict[str, Any]:
        """Convierte la entidad Customer a un diccionario."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "name": self.name,
            "email": self.email,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any], default_id: str = "") -> "Customer":
        """Crea una instancia de Customer a partir de un diccionario."""
        cust_id = str(data.get("id", default_id))
        email = str(data.get("email", ""))
        nombre = data.get("nombre") or data.get("name", "")
        return cls(id=cust_id, nombre=nombre, email=email)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Customer):
            return False
        return (
            self.id == other.id
            and self.email == other.email
            and self.nombre == other.nombre
        )

    def __repr__(self) -> str:
        return f"Customer(id={self.id!r}, nombre={self.nombre!r}, email={self.email!r})"
