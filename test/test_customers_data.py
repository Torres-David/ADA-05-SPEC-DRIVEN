import json
import os
import pytest

CUSTOMERS_FILE = os.path.join(os.path.dirname(__file__), "customers.json")


def load_customers():
    assert os.path.exists(CUSTOMERS_FILE), f"Database file not found: {CUSTOMERS_FILE}"
    with open(CUSTOMERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def test_customers_json_exists_and_is_valid():
    data = load_customers()
    assert isinstance(data, list), "Customer database should be a JSON list"


def test_customers_count_at_least_50():
    data = load_customers()
    assert len(data) >= 50, f"Expected at least 50 customers, got {len(data)}"


def test_no_duplicate_emails():
    data = load_customers()
    emails = [customer["email"].strip().lower() for customer in data]
    unique_emails = set(emails)
    assert len(emails) == len(unique_emails), f"Duplicate emails detected: {len(emails) - len(unique_emails)}"


def test_only_name_and_email_fields_present():
    data = load_customers()
    expected_fields = {"name", "email"}
    for customer in data:
        assert set(customer.keys()) == expected_fields, (
            f"Customer record must contain only 'name' and 'email', found: {set(customer.keys())}"
        )
        assert customer["name"] and isinstance(customer["name"], str), "Field 'name' must be a non-empty string"
        assert customer["email"] and isinstance(customer["email"], str), "Field 'email' must be a non-empty string"


def test_acceptance_criteria_seed_records_exist():
    data = load_customers()
    names = {customer["name"] for customer in data}
    emails = {customer["email"] for customer in data}

    # AC-01: Carlos Santana, Ana Martínez
    assert "Carlos Santana" in names
    assert "Ana Martínez" in names

    # AC-02: José Gómez
    assert "José Gómez" in names

    # AC-04: soporte.ti@empresa.com
    assert "soporte.ti@empresa.com" in emails

    # AC-06: Ana, Anabel, Mariana
    assert "Ana" in names
    assert "Anabel" in names
    assert "Mariana" in names
