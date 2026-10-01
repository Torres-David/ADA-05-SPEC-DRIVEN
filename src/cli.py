import argparse
import sys
from typing import Any, Dict

from handler import CustomerSearchHandler


def format_search_results(response: Dict[str, Any]) -> str:
    """Formatea la respuesta de búsqueda para salida en consola (CLI)."""
    status = response.get("status", 500)
    message = response.get("message", "")
    data = response.get("data", [])
    total = response.get("total", 0)
    page = response.get("page", 1)
    limit = response.get("limit", 20)
    order = response.get("order", "asc")

    lines = []
    lines.append(f"[{status}] {message}")

    if status == 200:
        lines.append(
            f"Resultados encontrados: {total} (Página {page}, Límite {limit}, Orden {order})"
        )
        lines.append("-" * 65)
        lines.append(f"{'ID':<6} | {'NOMBRE':<30} | {'CORREO ELECTRÓNICO':<30}")
        lines.append("-" * 65)
        for item in data:
            cust_id = str(item.get("id", ""))
            name = str(item.get("name", ""))
            email = str(item.get("email", ""))
            lines.append(f"{cust_id:<6} | {name:<30} | {email:<30}")
        lines.append("-" * 65)
    elif status == 404:
        lines.append(f"Información: {message}")
    else:
        lines.append(f"Error ({status}): {message}")

    return "\n".join(lines)


def main():
    """Punto de entrada CLI para búsqueda de clientes."""
    parser = argparse.ArgumentParser(
        description="CLI para la búsqueda de clientes (Customer Search)"
    )
    parser.add_argument(
        "query",
        nargs="?",
        default=None,
        help="Término de búsqueda general (nombre o correo)",
    )
    parser.add_argument("--name", help="Búsqueda específica por nombre")
    parser.add_argument("--email", help="Búsqueda específica por correo")
    parser.add_argument(
        "--page", type=int, default=1, help="Número de página para paginación (defecto: 1)"
    )
    parser.add_argument(
        "--limit", type=int, default=20, help="Cantidad de resultados por página (defecto: 20)"
    )
    parser.add_argument(
        "--order",
        choices=["asc", "desc"],
        default="asc",
        help="Orden de desempate alfabético por nombre ('asc' o 'desc', defecto: 'asc')",
    )

    args = parser.parse_args()
    handler = CustomerSearchHandler()

    if args.query or args.name or args.email:
        payload = {}
        if args.query:
            payload["query"] = args.query
        if args.name:
            payload["name"] = args.name
        if args.email:
            payload["email"] = args.email

        response = handler.handle(
            payload, page=args.page, limit=args.limit, order=args.order
        )
        print(format_search_results(response))
        return

    # Modo interactivo en CLI
    print("=" * 65)
    print("  CUSTOMER SEARCH CLI - Modo Interactivo")
    print("  (Escriba 'salir' o presione Ctrl+C para finalizar)")
    print("=" * 65)

    try:
        while True:
            term = input("\nIngrese término de búsqueda: ").strip()
            if term.lower() in ("salir", "exit", "quit"):
                print("Finalizando CLI...")
                break
            if not term:
                print("Por favor ingrese un término no vacío.")
                continue

            response = handler.handle({"query": term})
            print(format_search_results(response))
    except (KeyboardInterrupt, EOFError):
        print("\nSesión finalizada.")


if __name__ == "__main__":
    main()
