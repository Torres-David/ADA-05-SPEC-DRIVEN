# Repository Map
ADA-08 · Agent-Ready Repository · Ingeniería de Software asistida por IA

Quick index to answer: *"Where is what I need?"*

## Entry Points
- `src/cli.py` - Command-line interface and interactive query runner
- `src/handler.py` - Request handler, rate limiting (NFR-02), and HTTP response packaging
- `src/search_services.py` - Core search service, relevance scoring (AC-01..AC-06), text normalization
- `src/customer.py` - Customer domain entity model
- `src/customer_repository.py` - Data persistence loading `src/customers.json`
- `src/exceptions.py` - Domain and service error hierarchy (400, 404, 429, 500)

## Tests
- `test/test_customer.py` - Customer entity unit tests
- `test/test_customers_data.py` - Seed data integrity and uniqueness verification
- `test/test_search_service.py` - Search criteria logic and acceptance criteria (AC-01..AC-06, CR-01)
- `test/test_nfr.py` - Non-functional requirements (NFR-01 latency, NFR-02 rate limiting)
- `test/test_validation_and_errors.py` - Error trapping, empty query validation, 404/500 handling
- `test/test_validate_review_report.py` - Pull request readiness report validator tests

## Task & Specification Documents
- `REQUIREMENTS.md` - Functional (FR-01..FR-06) and non-functional requirements (NFR-01..NFR-03)
- `SPEC.md` - Technical specification, domain model, search scoring rules, acceptance criteria
- `ARCHITECTURE.md` - Architectural layers, responsibilities, and data flow
- `TASK_UNDER_TEST.md` - Active change request specification (precedes TASKS.md when present)
- `TASKS.md` - Project backlog and historical tasks (T-01..T-07)

## Change Guide
If modifying search or API behavior:
1. Check `REQUIREMENTS.md` / `SPEC.md` / `TASK_UNDER_TEST.md` for verifiable behavior.
2. Update `src/search_services.py` (service layer) and `src/handler.py` (handler layer).
3. Update domain (`src/customer.py`) only if entity attributes change.
4. Update CLI (`src/cli.py`) if parameter flags or display formatting change.
5. Add or update automated tests in `test/`.
6. Run `./scripts/verify_repo.sh` (or `python scripts/verify_repo.py`).

## Do Not Edit Directly
- `REQUIREMENTS.md` - Protected source of truth for business requirements
- `SPEC.md` - Protected source of truth for verifiable behavior
- `.env` - Environment secrets
- `results/` - Machine-generated evidence logs and test reports
