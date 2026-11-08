# Independent Review Report

## Review Context
Change ID: CR-02
Branch / PR: ada09/cr-02
Commit reviewed: c85575adaf89c153f85fb4791e7bd254403ea4de
Reviewer agent: Antigravity Independent Reviewer
Model: Gemini 3.8 Flash
Tools / permissions: read_file, run_command (read-only inspection and deterministic verification execution)

## Requirements / Acceptance Criteria Reviewed
### Requirements Reviewed - FR-04, FR-06 - AC-04, AC-07
- **FR-04**: The system must return records where the entered text partially matches the customer's email field (at least 3 characters in matching order).
- **FR-06**: Ability to perform customer searches via email address.
- **AC-04**: Search matching against customer email addresses (`soporte.ti@empresa.com`).
- **AC-07 (CR-02)**: When `email_domain` is specified (e.g. `'empresa.com'`), candidate matches are restricted to customer records under that domain. Leading `'@'` characters and whitespace are stripped, and comparison is case-insensitive. Invalid domain formats raise `ValidationError` (HTTP 400 Bad Request). If database matches exist for the query but none match the domain, HTTP 404 (`CustomerNotFoundError`) is returned with the exact FR-03 message. Omission or `None` preserves cross-domain matching.

## Verification Evidence Reviewed
### Test Evidence
1. **Automated Test Suite (`pytest -q`)**:
   - Total tests executed: 84
   - Passed: 84 / 84 (0.22s)
   - Pre-existing regression tests: 77 passed without modifications.
   - New automated tests for CR-02: 7 passed in `test/test_search_service.py`:
     - `test_email_domain_filter_scopes_results_to_specified_domain`
     - `test_email_domain_filter_excludes_non_matching_domains`
     - `test_email_domain_normalization_leading_at_and_case_insensitive`
     - `test_email_domain_via_payload_dictionary`
     - `test_email_domain_invalid_format_raises_validation_error`
     - `test_email_domain_in_handler_invocation`
     - `test_email_domain_none_or_omitted_preserves_cross_domain`
2. **Bytecode Compilation & Static Lint (`python -m compileall -q src test scripts`)**:
   - Result: Clean compilation across all modules (0 syntax or import errors).
3. **Repository Contract & Guardrails (`python scripts/check_repo_contract.py`)**:
   - Result: 7/7 checks passed (essential files, SPEC traceability, AGENTS contract commands, link integrity, seed DB schema).
4. **Secret Scanner Audit**:
   - Result: 0 sensitive credentials, API keys, or private keys detected in repository.
5. **Diff Analysis (`results/pr.diff`)**:
   - 6 files inspected: `CHANGE_REQUEST.md`, `scripts/check_repo_contract.py`, `src/cli.py`, `src/handler.py`, `src/search_services.py`, `test/test_search_service.py`.

## Findings

## MUST FIX
None. No violations of approved acceptance criteria, regressions in existing tests, architectural boundary leaks, or data integrity hazards were detected.

## SHOULD FIX

### RF-01 — SHOULD FIX
Category: Input Validation / Error Contract
Requirement / AC: AC-07 / SPEC.md line 37 ("Invalid formats raise ValidationError (HTTP 400)")
File / Line: [src/search_services.py:166-179](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/search_services.py#L166-L179)
Evidence:
`SPEC.md` (Validation Rules, line 37) states:
> "Email domain (CR-02): must be a non-empty string without whitespace, containing at least one dot separating domain and TLD (e.g. 'empresa.com'). Invalid formats raise ValidationError (HTTP 400)."

In `src/search_services.py`, lines 166-179:
```python
stripped_domain = raw_email_domain.strip().lower()
if stripped_domain.startswith("@"):
    stripped_domain = stripped_domain[1:].strip()
if (
    not stripped_domain
    or " " in stripped_domain
    or "." not in stripped_domain
    or stripped_domain.startswith(".")
    or stripped_domain.endswith(".")
):
    raise ValidationError(
        "El parámetro email_domain debe ser un dominio válido (ej. 'empresa.com')"
    )
clean_email_domain = stripped_domain
```
When a caller supplies a full email address or multiple `@` signs as the domain filter:
```python
service.search("Carlos", email_domain="user@empresa.com")
service.search("Carlos", email_domain="@@empresa.com")
```
1. `"user@empresa.com"` contains no spaces, has a dot, and does not start/end with a dot. It bypasses validation without raising `ValidationError`.
2. `"@@empresa.com"` has only one `@` removed by `if stripped_domain.startswith("@"): stripped_domain = stripped_domain[1:]`, leaving `"@empresa.com"`, which also bypasses validation.
3. In line 198:
```python
if "@" not in cust_email or cust_email.split("@")[-1] != clean_email_domain:
    continue
```
`"empresa.com" != "user@empresa.com"` evaluates to `True`, skipping valid records. Because zero records match, line 218 raises `CustomerNotFoundError(trimmed_term)`, causing `search()` to return **HTTP 404 Not Found** instead of **HTTP 400 Bad Request**.

Problem: The format validation check fails to reject strings containing internal `@` characters or multiple leading `@` characters, violating the error contract of SPEC.md.
Risk: Clients sending invalid domain filters receive HTTP 404 (indicating the customer does not exist) rather than HTTP 400 (indicating bad input), misleading client applications and masking client bugs.
Recommended next step:
Update `src/search_services.py` to strip all leading `@` characters and reject any remaining `@`:
```python
stripped_domain = raw_email_domain.strip().lower().lstrip("@").strip()
if (
    not stripped_domain
    or " " in stripped_domain
    or "@" in stripped_domain
    or "." not in stripped_domain
    or stripped_domain.startswith(".")
    or stripped_domain.endswith(".")
):
    raise ValidationError(
        "El parámetro email_domain debe ser un dominio válido (ej. 'empresa.com')"
    )
```

### RF-02 — SHOULD FIX
Category: Test Coverage / Interface Verification
Requirement / AC: AC-07 / AGENTS.md ("Definition of Done: Relevant tests pass. Acceptance criteria are covered and verified.")
File / Line: [src/cli.py:18-27](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/cli.py#L18-L27), [src/cli.py:76-80](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/cli.py#L76-L80), [src/cli.py:94-102](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/cli.py#L94-L102)
Evidence:
`src/cli.py` was modified in `results/pr.diff` (lines 304-336) to add CLI support:
```python
# Line 18-19:
email_domain = response.get("email_domain")
domain_suffix = f", Dominio @{email_domain}" if email_domain else ""

# Line 77-80:
parser.add_argument(
    "--email-domain",
    default=None,
    help="Filtrar resultados exclusivamente por dominio de correo electrónico (ej. 'empresa.com')",
)

# Line 100:
email_domain=args.email_domain,
```
However, an audit of all test files in `test/` shows:
```
test/test_check_repo_contract.py
test/test_customer.py
test/test_customers_data.py
test/test_nfr.py
test/test_search_service.py
test/test_validate_review_report.py
test/test_validation_and_errors.py
```
None of these test files import `src.cli` or invoke `format_search_results()` or `main()`. A search across the test suite (`git grep "cli" test/`) reveals zero assertions on CLI argument parsing or CLI output formatting.

Problem: The new `--email-domain` CLI option and its corresponding visual output formatting (`domain_suffix`) have no automated regression test coverage.
Risk: Breaking changes to argument parsing, flag names, or console formatting in `src/cli.py` will not be detected by `pytest`.
Recommended next step:
Add a dedicated test file `test/test_cli.py` or unit tests verifying:
1. `format_search_results()` includes `", Dominio @empresa.com"` when `email_domain="empresa.com"`.
2. `main()` correctly parses `--email-domain empresa.com` and passes it to `CustomerSearchHandler.handle()`.

## OPTIONAL

### RF-03 — OPTIONAL
Category: Maintainability / Code Duplication
Requirement / AC: ARCHITECTURE.md ("Design Decisions: Se decidio esta arquitectura para facilitar el principio de una sola responsabilidad, la revision y mantenibilidad del codigo.")
File / Line: [src/search_services.py:166-168](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/search_services.py#L166-L168) and [src/search_services.py:289-295](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/search_services.py#L289-L295)
Evidence:
In `src/search_services.py` (lines 166-168):
```python
stripped_domain = raw_email_domain.strip().lower()
if stripped_domain.startswith("@"):
    stripped_domain = stripped_domain[1:].strip()
```
And in `src/search_services.py` (lines 289-295, inside the `except CustomerNotFoundError` handler):
```python
resolved_email_domain: Optional[str] = None
if raw_domain is not None and isinstance(raw_domain, str):
    cleaned_domain = raw_domain.strip().lower()
    if cleaned_domain.startswith("@"):
        cleaned_domain = cleaned_domain[1:].strip()
    resolved_email_domain = cleaned_domain
```
Problem: String normalization for `email_domain` is duplicated across two methods in the same class.
Risk: If normalization logic is updated in `search_customers()`, the 404 response payload generator in `search()` may fall out of sync, returning differently formatted domain strings on errors.
Recommended next step:
Extract a private helper `_normalize_domain(raw_domain: Optional[str]) -> Optional[str]` to centralize normalization logic.

### RF-04 — OPTIONAL
Category: User Experience / Consistency
Requirement / AC: CLI Interactive Mode
File / Line: [src/cli.py:112-123](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/cli.py#L112-L123)
Evidence:
In `src/cli.py`, lines 112-123:
```python
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
```
Problem: While `src/cli.py` accepts `--email-domain` when invoked via arguments, interactive loop mode only prompts for a search term and does not allow users to specify an `email_domain`.
Risk: Users running the CLI interactively cannot access the domain filter feature.
Recommended next step:
Add an optional prompt or command syntax in the interactive loop (e.g. `Ingrese dominio de correo (opcional): `) to enable domain filtering in interactive sessions.

## Missing Evidence / Open Questions
None. The PR diff, specifications, architectural guidelines, production code, and all 84 automated tests were fully verified in the local environment.

## Summary
### Final Review Summary
MUST FIX count: 0
SHOULD FIX count: 2
OPTIONAL count: 2
Human decision required: YES

## Reviewer Recommendation
[ ] NOT READY
[ ] READY AFTER MUST FIX
[x] READY FOR HUMAN REVIEW

This recommendation is not a merge approval.
