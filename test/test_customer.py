import pytest
from src.customer import Customer


def test_customer_creation_with_attributes():
    customer = Customer(id="1", nombre="Carlos Santana", email="carlos.santana@example.com")
    assert customer.id == "1"
    assert customer.nombre == "Carlos Santana"
    assert customer.email == "carlos.santana@example.com"
    assert customer.name == "Carlos Santana"


def test_customer_creation_with_email_and_nombre_order():
    # TASKS.md specifies "Usuario con id, email y nombre"
    customer = Customer("1", "carlos.santana@example.com", "Carlos Santana")
    assert customer.id == "1"
    assert customer.email == "carlos.santana@example.com"
    assert customer.nombre == "Carlos Santana"
    assert customer.name == "Carlos Santana"


def test_customer_creation_with_nombre_and_email_order():
    # SPEC.md specifies Customer { id, nombre, email }
    customer = Customer("1", "Carlos Santana", "carlos.santana@example.com")
    assert customer.id == "1"
    assert customer.nombre == "Carlos Santana"
    assert customer.email == "carlos.santana@example.com"
    assert customer.name == "Carlos Santana"


def test_customer_creation_with_name_keyword():
    customer = Customer(id="2", name="Ana Martínez", email="ana.martinez@example.com")
    assert customer.id == "2"
    assert customer.nombre == "Ana Martínez"
    assert customer.name == "Ana Martínez"
    assert customer.email == "ana.martinez@example.com"


def test_customer_name_setter():
    customer = Customer(id="3", nombre="José", email="jose@example.com")
    customer.name = "José Gómez"
    assert customer.nombre == "José Gómez"
    assert customer.name == "José Gómez"


def test_customer_to_dict():
    customer = Customer(id="1", nombre="Carlos Santana", email="carlos.santana@example.com")
    d = customer.to_dict()
    assert d == {
        "id": "1",
        "nombre": "Carlos Santana",
        "name": "Carlos Santana",
        "email": "carlos.santana@example.com",
    }


def test_customer_from_dict():
    data = {"name": "Carlos Santana", "email": "carlos.santana@example.com"}
    customer = Customer.from_dict(data, default_id="cust-01")
    assert customer.id == "cust-01"
    assert customer.nombre == "Carlos Santana"
    assert customer.name == "Carlos Santana"
    assert customer.email == "carlos.santana@example.com"


def test_customer_equality():
    c1 = Customer(id="1", nombre="Ana", email="ana@example.com")
    c2 = Customer(id="1", nombre="Ana", email="ana@example.com")
    c3 = Customer(id="2", nombre="Ana", email="ana@example.com")
    assert c1 == c2
    assert c1 != c3
    assert c1 != "not a customer"


def test_customer_repr():
    customer = Customer(id="1", nombre="Ana", email="ana@example.com")
    assert repr(customer) == "Customer(id='1', nombre='Ana', email='ana@example.com')"
