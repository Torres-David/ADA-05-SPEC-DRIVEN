# Technical Report — Task Under Test (CR-01)

## Clarification Questions Requested by the Agent
- **None requested.** The project context, architectural layers, and specifications provided in `REQUIREMENTS.md`, `SPEC.md`, `ARCHITECTURE.md`, `TASKS.md`, and `TASK_UNDER_TEST.md` provided sufficient, unambiguous requirements to execute the task safely without requiring additional clarification.

---

## Files Explored to Understand the Repository
1. `TASK_UNDER_TEST.md`: Definition and verification criteria for change `CR-01` (adding optional `search_field` parameter supporting `'all'`, `'name'`, and `'email'`).
2. `REQUIREMENTS.md`: Functional requirements (`FR-01` to `FR-06`) and non-functional requirements (`NFR-01` latency $\le$ 300 ms, `NFR-02` rate limiting 30 req/min, `NFR-03` accessibility).
3. `SPEC.md`: Customer domain model, search relevance scoring rules (1: exact name, 2: exact email, 3: prefix name, 4: prefix email, 5: substring name, 6: substring email), error handling guidelines, and acceptance criteria (`AC-01` to `AC-06`).
4. `ARCHITECTURE.md`: Layered architecture documentation (`Handler` $\to$ `Service` $\to$ `Domain` / `Repository`), request interfaces, and design decisions.
5. `TASKS.md`: Project task history covering setup (`T-01`), domain model (`T-02`), search logic (`T-03`), validation (`T-04`), tests (`T-05`), documentation (`T-06`), and sort order (`T-07`).
6. `README.md`: User-facing documentation detailing CLI commands, programmatic usage, error response formats, and testing procedures.
7. `pytest.ini`: Pytest configuration setting `pythonpath = . src`.
8. `src/exceptions.py`: Exception hierarchy (`CustomerSearchException`, `EmptyQueryError`, `ValidationError`, `CustomerNotFoundError`, `DatabaseError`, `RateLimitExceededError`).
9. `src/customer.py`: `Customer` domain entity with `id`, `nombre`/`name`, and `email` properties.
10. `src/customer_repository.py`: File-based repository loading customer entities from `customers.json`.
11. `src/search_services.py`: Core search service orchestrating text normalization, relevance scoring, pagination, and error trapping.
12. `src/handler.py`: Request handler implementing sliding-window rate limiting and service dispatch.
13. `src/cli.py`: Command-line entry point with interactive prompt and argument parsing via `argparse`.
14. `src/customers.json`: Seed dataset consisting of 52 unique customer records.
15. `test/test_customer.py`: Unit tests for entity construction, serialization, and equality.
16. `test/test_customers_data.py`: Data integrity tests verifying seed records for acceptance criteria.
17. `test/test_nfr.py`: Performance latency tests under concurrent load and user rate limiting verification.
18. `test/test_search_service.py`: Acceptance criteria tests (`AC-01` through `AC-06`) and service behavior tests.
19. `test/test_validation_and_errors.py`: Tests for empty query, short query, 404, and database error trapping.
20. `test/test_validate_review_report.py`: Tests for the PR review validator script.
21. `scripts/validate_review_report.py`: Deterministic validator for PR readiness reviews.
22. `results/agent-report.md`: Historical report tracking task implementation stages.

---

## Incorrect Assumptions
1. **Tool String Replacement Assumption on Windows Line Endings**:
   - *Assumption*: The `edit_file` tool would match multiline targets assuming Unix `\n` line endings.
   - *Correction*: The repository files were authored with Windows CRLF (`\r\n`) line terminators. Direct text matching failed; resolved by reading the file and using consistent file writing operations that preserve appropriate encoding.
2. **Assumption Regarding Git Command Execution**:
   - *Assumption*: Running `git status` to verify modified files was acceptable as general inspection.
   - *Correction*: The user explicitly instructed not to run git inspection commands when not part of the scope (`"No revisar git status ni nada de git si no es parte del alcance de lo indicado"`). The command was stopped and no further git commands were run.
3. **Payload Parameter Scoping Assumption**:
   - *Assumption*: `request_payload.get("name")` or `request_payload.get("email")` might have previously scoped queries.
   - *Correction*: Inspection revealed that previous implementations only extracted the search query string from those keys, but evaluated both name and email fields uniformly. Scoping required explicit condition filtering controlled by the `search_field` parameter.

---

## Failed or Unknown Commands
1. `edit_file` on `src/search_services.py`:
   - *Outcome*: Failed (`target content not found in the file; the Target must exactly match existing file text, including whitespace`).
   - *Root Cause*: Windows CRLF (`\r\n`) vs Unix LF (`\n`) mismatch in multiline payload.
   - *Remediation*: Replaced with `write_file` supplying the complete file content.
2. `git status --short`:
   - *Outcome*: Permission denied by user.
   - *Root Cause*: User policy restriction explicitly disallowing git status inspection.
   - *Remediation*: Ceased all git command usage.
3. `python src/cli.py "emp" --search-field invalid`:
   - *Outcome*: Process exited with exit code 1.
   - *Root Cause*: Intentional verification command demonstrating that `argparse` correctly rejects invalid choices (`--search-field: invalid choice: 'invalid' (choose from 'all', 'name', 'email')`).

---

## Out-of-Scope Files Modified
- **None.** Only files directly required to implement, validate, and document change `CR-01` were modified:
  - `src/search_services.py` (in-scope: implementation of `search_field` parameter, relevance evaluation filter, validation)
  - `src/handler.py` (in-scope: handler parameter propagation)
  - `src/cli.py` (in-scope: CLI `--search-field` option and result formatting)
  - `test/test_search_service.py` (in-scope: automated test coverage for `CR-01`)
  - `TASKS.md` (in-scope: task traceability for `T-08`)
  - `README.md` (in-scope: user documentation reflecting final behavior)
  - `results/before-agent-run.md` (in-scope: required technical evidence report)

---

## Tests/Validations Executed or Skipped

### 1. Pre-Change Baseline Validation
- **Command executed**: `pytest`
- **Result**: 61 passed in 0.17s.

### 2. Post-Change Automated Test Suite
- **Command executed**: `pytest -v`
- **Result**: 69 passed in 0.17s (0 failed, 0 skipped, 0 regressions).
- **Test summary by file**:
  - `test/test_customer.py`: 9 passed
  - `test/test_customers_data.py`: 5 passed
  - `test/test_nfr.py`: 3 passed
  - `test/test_search_service.py`: 29 passed (21 pre-existing + 8 new `CR-01` tests)
  - `test/test_validate_review_report.py`: 14 passed
  - `test/test_validation_and_errors.py`: 9 passed

### 3. New Tests Added for CR-01
- `test_search_field_name_scoping`: Verifies `search_field='name'` matches only on customer names and excludes records matching only on emails.
- `test_search_field_email_scoping`: Verifies `search_field='email'` matches only on customer emails and excludes records matching only on names.
- `test_search_field_all_and_omitted_matches_both`: Verifies `search_field='all'` or omitted preserves cross-field matching and backward compatibility.
- `test_search_field_via_payload_dictionary`: Verifies parameter delivery via request payload dictionary (`{"query": "...", "search_field": "..."}`).
- `test_search_field_invalid_value_raises_validation_error`: Verifies invalid `search_field` values raise `ValidationError` in service and yield HTTP 400 response.
- `test_search_field_in_handler_invocation`: Verifies parameter reception via `CustomerSearchHandler.handle()` arguments and payload dictionary.
- `test_search_field_scoping_with_seed_database`: Verifies scoping using the full 52-record database (`customers.json`), testing that term `'emp'` matches Soporte TI under `'email'` and `'all'`, but returns HTTP 404 under `'name'`.
- `test_search_field_case_insensitivity_and_none_default`: Verifies casing and whitespace normalization (e.g., `' NAME '` $\to$ `'name'`) and `None` fallback to `'all'`.

### 4. CLI Runtime Validations
- `python src/cli.py "Carlos" --search-field name`: HTTP 200, returns Carlos Santana.
- `python src/cli.py "emp" --search-field name`: HTTP 404, excludes email-only match Soporte TI.
- `python src/cli.py "emp" --search-field email`: HTTP 200, returns Soporte TI (`soporte.ti@empresa.com`).
- `python src/cli.py "emp" --search-field all`: HTTP 200, returns Soporte TI.
- `python src/cli.py "emp" --search-field invalid`: Error 2, invalid choice rejected.

### 5. Skipped Tests
- **None.** All 69 tests were executed and passed.

---

## Final Result: PASS / PARTIAL / FAIL
**PASS**

All requirements from `TASK_UNDER_TEST.md` (Change ID `CR-01`) have been fully satisfied:
- Optional `search_field` parameter implemented supporting `'all'`, `'name'`, and `'email'` (defaulting to `'all'`).
- Query evaluation scopes strictly according to `search_field`.
- Default cross-field matching and backward compatibility preserved with zero regressions across pre-existing suites.
- Unsupported values raise `ValidationError` / return HTTP 400 Bad Request.
- Parameter accepted via payload dictionary, service method call, handler invocation, and CLI.
- 100% test pass rate (69/69 tests passing).
