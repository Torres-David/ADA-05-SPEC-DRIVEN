import pytest
from src.customer import Customer
from src.customer_repository import CustomerRepository
from src.exceptions import (
    CustomerNotFoundError,
    EmptyQueryError,
    ValidationError,
)
from src.handler import CustomerSearchHandler
from src.search_services import CustomerSearchService, normalize_text


@pytest.fixture
def service():
    """Instancia del servicio cargando la base de datos simulada customers.json."""
    return CustomerSearchService()


def test_normalize_text():
    assert normalize_text("José Gómez") == "jose gomez"
    assert normalize_text("CARLOS") == "carlos"
    assert normalize_text("  Ana Martínez  ") == "ana martinez"
    assert normalize_text("Pingüino") == "pinguino"
    assert normalize_text("") == ""


def test_ac01_substring_and_case_insensitive_matching(service):
    """AC-01: 'arl' or 'CARLOS' must return Carlos Santana."""
    result_arl = service.search({"name": "arl"})
    assert result_arl["status"] == 200
    names_arl = [c["name"] for c in result_arl["data"]]
    assert "Carlos Santana" in names_arl

    result_carlos = service.search({"name": "CARLOS"})
    assert result_carlos["status"] == 200
    names_carlos = [c["name"] for c in result_carlos["data"]]
    assert "Carlos Santana" in names_carlos


def test_ac02_accent_normalization(service):
    """AC-02: 'jose gomez' must return 'José Gómez'."""
    result = service.search({"query": "jose gomez"})
    assert result["status"] == 200
    names = [c["name"] for c in result["data"]]
    assert "José Gómez" in names


def test_ac04_email_partial_match(service):
    """AC-04: 'sop' or 'emp' returns 'soporte.ti@empresa.com'."""
    result_sop = service.search({"email": "sop"})
    assert result_sop["status"] == 200
    emails_sop = [c["email"] for c in result_sop["data"]]
    assert "soporte.ti@empresa.com" in emails_sop

    result_emp = service.search({"query": "emp"})
    assert result_emp["status"] == 200
    emails_emp = [c["email"] for c in result_emp["data"]]
    assert "soporte.ti@empresa.com" in emails_emp


def test_ac05_only_authorized_basic_fields_returned(service):
    """AC-05: Only id, name, email in result payload; no sensitive fields."""
    result = service.search({"query": "Carlos"})
    assert result["status"] == 200
    for item in result["data"]:
        assert set(item.keys()) == {"id", "name", "email"}
        assert "password_hash" not in item
        assert "tax_id" not in item


def test_ac06_strict_relevance_ordering():
    """AC-06: Strict relevance order: exact ('Ana') > prefix ('Anabel') > substring ('Mariana')."""
    customers = [
        Customer(id="3", nombre="Mariana", email="mariana@example.com"),
        Customer(id="2", nombre="Anabel", email="anabel@example.com"),
        Customer(id="1", nombre="Ana", email="ana@example.com"),
    ]
    service = CustomerSearchService(customers=customers)
    result = service.search({"query": "Ana"})
    assert result["status"] == 200
    names = [c["name"] for c in result["data"]]
    assert names == ["Ana", "Anabel", "Mariana"]


def test_fr03_no_results_returns_exact_message(service):
    """FR-03: When no match is found, show exact text: 'No se encontraron clientes para {término}'."""
    result = service.search({"query": "termino_inexistente_xyz"})
    assert result["status"] == 404
    assert result["message"] == "No se encontraron clientes para 'termino_inexistente_xyz'"
    assert result["data"] == []


def test_edge_case_empty_or_whitespace_query(service):
    """Empty or spaces-only queries are cancelled with 400 Bad Request."""
    result_empty = service.search("")
    assert result_empty["status"] == 400

    result_spaces = service.search({"query": "     "})
    assert result_spaces["status"] == 400


def test_edge_case_query_shorter_than_3_characters(service):
    """Queries under 3 characters are rejected according to 3-consecutive-character rule."""
    result = service.search("ab")
    assert result["status"] == 400
    assert "3 caracteres" in result["message"]


def test_edge_case_case_insensitivity_symmetry(service):
    """SPEC.md: 'carlos', 'Carlos', 'CARLOS' must return exactly the same set of results."""
    res_lower = service.search("carlos")
    res_title = service.search("Carlos")
    res_upper = service.search("CARLOS")

    assert res_lower["status"] == 200
    assert res_lower["data"] == res_title["data"]
    assert res_title["data"] == res_upper["data"]


def test_search_rules_alphabetical_tie_breaker():
    """SPEC.md: If two items share the same match priority, alphabetical order is used."""
    customers = [
        Customer(id="2", nombre="Carlos Valderrama", email="carlos.v@example.com"),
        Customer(id="1", nombre="Carlos Santana", email="carlos.s@example.com"),
        Customer(id="3", nombre="Carlos Alberto", email="carlos.a@example.com"),
    ]
    custom_service = CustomerSearchService(customers=customers)
    res = custom_service.search("Carlos")
    assert res["status"] == 200
    names = [c["name"] for c in res["data"]]
    assert names == ["Carlos Alberto", "Carlos Santana", "Carlos Valderrama"]


def test_architecture_request_interface(service):
    """ARCHITECTURE.md: Request interface { 'email': ..., 'name': ... }."""
    payload = {"email": "carlos.santana@example.com", "name": "Carlos"}
    res = service.search(payload)
    assert res["status"] == 200
    assert len(res["data"]) >= 1
    assert res["data"][0]["name"] == "Carlos Santana"


def test_happy_path_exact_match(service):
    """SPEC.md Happy path: The system finds an exact register."""
    res = service.search("Carlos Santana")
    assert res["status"] == 200
    assert len(res["data"]) >= 1
    assert res["data"][0]["name"] == "Carlos Santana"


def test_pagination_limits_and_slices(service):
    """Constraints: Deliver in segments of 20 with pagination, and verify slicing."""
    res_page_1 = service.search("example.com", page=1, limit=5)
    res_page_2 = service.search("example.com", page=2, limit=5)

    assert res_page_1["status"] == 200
    assert res_page_2["status"] == 200
    assert len(res_page_1["data"]) == 5
    assert len(res_page_2["data"]) == 5

    names_p1 = [c["name"] for c in res_page_1["data"]]
    names_p2 = [c["name"] for c in res_page_2["data"]]
    # Los elementos de página 1 y página 2 no deben solaparse
    assert set(names_p1).isdisjoint(set(names_p2))


def test_service_domain_exceptions_explicitly_raised(service):
    """T-04/T-05: search_customers directly raises domain exceptions."""
    with pytest.raises(EmptyQueryError):
        service.search_customers("   ")

    with pytest.raises(ValidationError):
        service.search_customers("xy")

    with pytest.raises(CustomerNotFoundError):
        service.search_customers("registro_no_existente_999")


def test_service_traps_all_exceptions_to_http_codes(service):
    """T-05 Acceptance: El sistema atrapa correctamente los errores y responde con códigos HTTP."""
    # 400 por vacío
    assert service.search("")["status"] == 400
    # 400 por longitud
    assert service.search("12")["status"] == 400
    # 404 por no encontrado
    assert service.search("no_match_12345")["status"] == 404
    # 500 por error interno simulado
    broken_repo = CustomerRepository(db_path="invalid_path.json")
    broken_service = CustomerSearchService(repository=broken_repo)
    res_500 = broken_service.search("carlos")
    assert res_500["status"] == 500
    assert "Error interno del servidor" in res_500["message"]


def test_configurable_sort_order_ascending():
    """T-07: order='asc' (por defecto) ordena los empates de coincidencia alfabéticamente A-Z."""
    customers = [
        Customer(id="2", nombre="Carlos Valderrama", email="carlos.v@example.com"),
        Customer(id="1", nombre="Carlos Santana", email="carlos.s@example.com"),
        Customer(id="3", nombre="Carlos Alberto", email="carlos.a@example.com"),
    ]
    service = CustomerSearchService(customers=customers)
    res = service.search("Carlos", order="asc")
    assert res["status"] == 200
    assert res["order"] == "asc"
    names = [c["name"] for c in res["data"]]
    assert names == ["Carlos Alberto", "Carlos Santana", "Carlos Valderrama"]


def test_configurable_sort_order_descending():
    """T-07: order='desc' invierte el desempate alfabético a Z-A preservando los niveles de relevancia."""
    customers = [
        Customer(id="2", nombre="Carlos Valderrama", email="carlos.v@example.com"),
        Customer(id="1", nombre="Carlos Santana", email="carlos.s@example.com"),
        Customer(id="3", nombre="Carlos Alberto", email="carlos.a@example.com"),
    ]
    service = CustomerSearchService(customers=customers)
    res = service.search("Carlos", order="desc")
    assert res["status"] == 200
    assert res["order"] == "desc"
    names = [c["name"] for c in res["data"]]
    assert names == ["Carlos Valderrama", "Carlos Santana", "Carlos Alberto"]


def test_configurable_sort_order_via_payload():
    """T-07: El parámetro order puede ser suministrado dentro del request_payload."""
    customers = [
        Customer(id="2", nombre="Carlos Valderrama", email="carlos.v@example.com"),
        Customer(id="1", nombre="Carlos Santana", email="carlos.s@example.com"),
        Customer(id="3", nombre="Carlos Alberto", email="carlos.a@example.com"),
    ]
    service = CustomerSearchService(customers=customers)
    res = service.search({"query": "Carlos", "order": "desc"})
    assert res["status"] == 200
    assert res["order"] == "desc"
    names = [c["name"] for c in res["data"]]
    assert names == ["Carlos Valderrama", "Carlos Santana", "Carlos Alberto"]


def test_configurable_sort_order_invalid_value_raises_validation_error():
    """T-07: Valores de ordenamiento no permitidos lanzan ValidationError (HTTP 400)."""
    service = CustomerSearchService()
    with pytest.raises(ValidationError) as exc_info:
        service.search_customers("Carlos", order="invalido")
    assert exc_info.value.status_code == 400
    assert "El parámetro de ordenamiento debe ser 'asc' o 'desc'" in exc_info.value.message

    # Al usar search() se atrapa y retorna respuesta HTTP 400
    res = service.search({"query": "Carlos", "order": "invalido"})
    assert res["status"] == 400
    assert "El parámetro de ordenamiento debe ser 'asc' o 'desc'" in res["message"]


def test_configurable_sort_order_in_handler():
    """T-07: CustomerSearchHandler procesa y propaga correctamente el parámetro order."""
    handler = CustomerSearchHandler()
    res_asc = handler.handle({"name": "Carlos"}, order="asc")
    assert res_asc["status"] == 200
    assert res_asc["order"] == "asc"

    res_desc = handler.handle({"name": "Carlos"}, order="desc")
    assert res_desc["status"] == 200
    assert res_desc["order"] == "desc"

