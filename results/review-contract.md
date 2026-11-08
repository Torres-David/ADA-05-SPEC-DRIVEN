# Review Contract

## Change
CR-02

## Requirements / Acceptance Criteria
- FR-04: The system must return records where the entered text partially matches the customer's email field (at least 3 characters in matching order).
- FR-06: Se debe poder realizar búsquedas por medio de correo electrónico.
- AC-04: Partial match against customer email addresses (`soporte.ti@empresa.com`).
- AC-07 (CR-02): Optional `email_domain` parameter scopes matches to customers with that email domain, normalizes input (stripping leading `@` and lowercasing), rejects malformed domain formats with HTTP 400 Bad Request, and maintains cross-domain search when omitted.

## Architecture Constraints
- Expected dependency flow: `CLI (cli.py)` -> `Handler (handler.py)` -> `Service (search_services.py)` -> `Repository (customer_repository.py)` -> `Domain / Data (customer.py / customers.json)`. Calls must only flow downwards; responses return upward as sanitized DTO dictionaries.
- Business-rule location: `src/search_services.py` (`CustomerSearchService`) encapsulates all search filtering, relevance calculation, normalization, and input domain validation. `src/handler.py` manages rate limiting (NFR-02) and HTTP status code packaging.
- Protected boundaries: `src/customer_repository.py` and `src/customers.json` are read-only persistence; sensitive attributes (`password_hash`, `tax_id`) must never leak to the public DTO (FR-05, AC-05); `.env` secrets and specification sources of truth (`REQUIREMENTS.md`) are protected.

## Review Rules
- Verify requirement coverage.
- Verify every called API/dependency exists.
- Check architecture boundaries.
- Inspect tests for masking / false confidence.
- Check regression behavior.
- Identify unnecessary technical debt.
- Cite evidence for every finding.

## Severity
MUST FIX:
Requirement violation, regression, security/integrity risk,
hallucinated API/dependency, broken architecture constraint,
or defect that makes the change unsafe to approve.

SHOULD FIX:
Significant maintainability, coverage, design, or clarity issue
that does not block the requested behavior.

OPTIONAL:
Non-blocking improvement outside the minimum acceptance threshold.
