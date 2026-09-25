import os
import tempfile
import pytest

from src.customer_repository import CustomerRepository
from src.exceptions import (
    CustomerNotFoundError,
    DatabaseError,
    EmptyQueryError,
    ValidationError,
)
from src.handler import CustomerSearchHandler
from src.search_services import CustomerSearchService


def test_empty_query_error_raised():
    service = CustomerSearchService()
    with pytest.raises(EmptyQueryError) as exc_info:
        service.search_customers("   ")
    assert exc_info.value.status_code == 400
    assert "El término de búsqueda no puede estar vacío" in exc_info.value.message


def test_empty_query_response_code_400():
    handler = CustomerSearchHandler()
    response = handler.handle("")
    assert response["status"] == 400
    assert "no puede estar vacío" in response["message"]


def test_short_query_validation_error():
    service = CustomerSearchService()
    with pytest.raises(ValidationError) as exc_info:
        service.search_customers("ab")
    assert exc_info.value.status_code == 400
    assert "3 caracteres" in exc_info.value.message


def test_customer_not_found_error_raised():
    service = CustomerSearchService()
    with pytest.raises(CustomerNotFoundError) as exc_info:
        service.search_customers("cliente_inexistente_123")
    assert exc_info.value.status_code == 404
    assert exc_info.value.message == "No se encontraron clientes para 'cliente_inexistente_123'"


def test_customer_not_found_response_code_404():
    handler = CustomerSearchHandler()
    response = handler.handle({"query": "cliente_inexistente_123"})
    assert response["status"] == 404
    assert response["message"] == "No se encontraron clientes para 'cliente_inexistente_123'"
    assert response["data"] == []


def test_database_error_when_file_not_found():
    non_existent_path = "non_existent_customers_db.json"
    repo = CustomerRepository(db_path=non_existent_path)
    with pytest.raises(DatabaseError) as exc_info:
        repo.get_all()
    assert exc_info.value.status_code == 500
    assert "Base de datos no encontrada" in exc_info.value.message


def test_database_error_when_file_corrupted():
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json", encoding="utf-8") as temp_file:
        temp_file.write("INVALID JSON CONTENT { [ }")
        temp_path = temp_file.name

    try:
        repo = CustomerRepository(db_path=temp_path)
        with pytest.raises(DatabaseError) as exc_info:
            repo.get_all()
        assert exc_info.value.status_code == 500
        assert "Fallo al leer la base de datos" in exc_info.value.message
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_handler_catches_database_error_and_returns_500():
    repo = CustomerRepository(db_path="missing_db_file.json")
    service = CustomerSearchService(repository=repo)
    handler = CustomerSearchHandler(service=service)

    response = handler.handle({"name": "Carlos"})
    assert response["status"] == 500
    assert "Error interno" in response["message"]


def test_handler_successful_search_returns_200():
    handler = CustomerSearchHandler()
    response = handler.handle({"name": "Carlos Santana"})
    assert response["status"] == 200
    assert response["message"] == "Búsqueda exitosa"
    assert len(response["data"]) >= 1
    assert response["data"][0]["name"] == "Carlos Santana"
