# PR Evidence

## Change
- **Change ID**: CR-02
- **PR / Branch**: `ada09/cr-02`
- **Base commit**: `3e5df59b8386577a24cac5ec9783e0c4071e0093` (`main`) / initial branch commit `c85575adaf89c153f85fb4791e7bd254403ea4de`
- **Final commit**: `d936f47990e57eded36fd4ab335a58ccee8963fa`

## Requirements / Acceptance Criteria
- **FR-04**: The system must return records where the entered text partially matches the customer's email field (at least 3 characters in matching order).
- **FR-06**: Se debe poder realizar búsquedas por medio de correo electrónico.
- **AC-04**: Partial match against customer email addresses (`soporte.ti@empresa.com`).
- **AC-07 (CR-02)**: Optional `email_domain` filter parameter restricts candidate matches exclusively to customer records under the specified email domain (e.g. `'empresa.com'`). Normalization strips leading `'@'` characters, whitespace, and performs case-insensitive matching. Omission or `None` preserves cross-domain matching. Invalid domain formats raise `ValidationError` (HTTP 400 Bad Request). If database matches exist for the query but none match the domain, HTTP 404 (`CustomerNotFoundError`) is returned with the exact FR-03 message.

## Implementation
- **Coder report**: [`results/coder-report.md`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/results/coder-report.md)
- **Files changed**:
  - `src/search_services.py`: Extended `search_customers()` and `search()` with `email_domain` parameter, normalization, validation, filtering, and 404 response metadata.
  - `src/handler.py`: Added `email_domain` argument and forwarded it seamlessly to `service.search()`.
  - `src/cli.py`: Added `--email-domain` flag to parser, updated `format_search_results` with domain suffix, and added modular import fallback.
  - `test/test_search_service.py`: Added 9 automated tests covering scoping, exclusion, normalization, payload delivery, invalid format rejection, handler integration, cross-domain preservation, and CLI formatting.
  - `CHANGE_REQUEST.md`: Change request definition for CR-02.
  - `scripts/check_repo_contract.py`: Deterministic repository contract & guardrail checker.
- **Commits**:
  - `6ca926e`: `feat: implement CR-02`
  - `d936f47`: `fix: address ADA-09 review findings`

## Verification
- **Verification command**: `python scripts/verify_repo.py`
- **Final result**: **PASS**
- **Tests**: **86 passed** in 0.24s (77 regression tests + 9 tests for CR-02 / RF-01 / RF-02)
- **Lint**: `python -m compileall -q src test scripts` — PASS (0 errors across all directories)
- **Security / repo checks**: `python scripts/check_repo_contract.py` — PASS (7/7 guardrails passed; 0 sensitive keys or tokens detected)

## Independent Review
- **Review report**: [`results/review-report.md`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/results/review-report.md)
- **MUST FIX found**: 0
- **SHOULD FIX found**: 2
  - RF-01: Permissive domain format validation allowing `@` characters.
  - RF-02: Missing automated unit tests for `src/cli.py` `format_search_results`.
- **OPTIONAL found**: 2
  - RF-03: Code duplication in 404 handler domain extraction.
  - RF-04: CLI interactive loop does not prompt for domain filter.

## Human Decisions
Documented in [`results/human-review-decisions.md`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/results/human-review-decisions.md):
- **Accepted**: **RF-01** — Validations must strictly reject internal `@` or multiple leading `@` with HTTP 400 Bad Request.
- **Modified**: **RF-02** — Scope unit tests directly to `format_search_results` output formatting with and without domain filter.
- **Rejected**: **RF-04** — Interactive loop UX is outside the defined scope of CR-02.
- **Deferred**: **RF-03** — Minor code duplication in 404 handler deferred to backlog as technical debt.

## Re-review
Documented in [`results/re-review-report.md`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/results/re-review-report.md):
- **Resolved**: 2 (RF-01, RF-02)
- **Partially resolved**: 0
- **Not resolved**: 0
- **New MUST FIX**: 0

## Traceability

| Requirement / AC | Task / Change | Code | Test | Review Finding |
|---|---|---|---|---|
| **FR-04** | Email partial matching preserved under domain scoping | [`src/search_services.py:192-208`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/search_services.py#L192-L208) | [`test/test_search_service.py:407-416`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/test/test_search_service.py#L407-L416) | N/A (Verified compliant) |
| **FR-06** | Search via email domain filter parameter | [`src/search_services.py:116,133`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/search_services.py#L116), [`src/handler.py:75,112`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/handler.py#L75) | [`test/test_search_service.py:469-482`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/test/test_search_service.py#L469-L482) | N/A (Verified compliant) |
| **AC-04** | Match against customer email records (`soporte.ti@empresa.com`) | [`src/search_services.py:194-208`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/search_services.py#L194-L208) | [`test/test_search_service.py:440-447`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/test/test_search_service.py#L440-L447) | N/A (Verified compliant) |
| **AC-07 (CR-02)** | Domain scoping & non-matching domain exclusion | [`src/search_services.py:196-200`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/search_services.py#L196-L200) | [`test/test_search_service.py:418-430`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/test/test_search_service.py#L418-L430) | N/A (Verified compliant) |
| **AC-07 (CR-02)** | Domain normalization (`@` strip, lowercase, trim) | [`src/search_services.py:166-169`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/search_services.py#L166-L169) | [`test/test_search_service.py:432-438`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/test/test_search_service.py#L432-L438) | N/A (Verified compliant) |
| **AC-07 (CR-02)** | Domain format validation (HTTP 400 rejection) | [`src/search_services.py:170-179`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/search_services.py#L170-L179) | [`test/test_search_service.py:449-467`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/test/test_search_service.py#L449-L467) | **RF-01** (RESOLVED) |
| **AC-07 (CR-02)** | Cross-domain search preservation when omitted / None | [`src/search_services.py:196,245`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/search_services.py#L196) | [`test/test_search_service.py:484-493`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/test/test_search_service.py#L484-L493) | N/A (Verified compliant) |
| **AC-07 (CR-02)** | CLI formatting with active domain filter | [`src/cli.py:18-20,26`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/cli.py#L18-L20) | [`test/test_search_service.py:497-534`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/test/test_search_service.py#L497-L534) | **RF-02** (RESOLVED) |
| **AC-07 (CR-02)** | Domain metadata included in HTTP 404 response | [`src/search_services.py:277,304`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/src/search_services.py#L277) | [`test/test_search_service.py:425-430`](file:///D:/IGNITER/Documents/Proyectos/ADA-05-SPEC-DRIVEN/test/test_search_service.py#L425-L430) | **RF-03** (DEFERRED) |

## Remaining Risks / Technical Debt
- **RF-03 (Technical Debt)**: Minor duplication of string normalization logic in `search()` exception handling (lines 289-295 of `src/search_services.py`). Tracked for a future cleanup refactor.
- **Single-Domain Filter Boundary**: The filter accepts one domain at a time (e.g. `'empresa.com'`). Multi-domain filtering (e.g. comma-separated domains) is intentionally out of scope for CR-02.

## Final Human Decision
[ ] NOT READY  
[x] READY FOR HUMAN MERGE  

Approved by: David Torres  
Date: 08/11/2026
