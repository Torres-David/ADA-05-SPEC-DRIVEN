# Task Under Test

Change ID: CR-01

## Goal
Add an optional `search_field` parameter to the customer search interface supporting values `'all'`, `'name'`, and `'email'` (defaulting to `'all'`), allowing callers to scope matches specifically to customer names or email addresses while preserving default cross-field search behavior and backward compatibility.

## Requirements Covered
- FR-01
- FR-04
- FR-06
- AC-01
- AC-04

## Verification
- When `search_field='name'`, query evaluation matches only against customer names; records matching only on email addresses are excluded.
- When `search_field='email'`, query evaluation matches only against customer emails; records matching only on names are excluded.
- When `search_field='all'` or omitted, query evaluation matches against both name and email fields, maintaining existing behavior and backwards compatibility.
- Any unsupported `search_field` value raises a `ValidationError` resulting in an HTTP 400 Bad Request response.
- The parameter is accepted via payload dictionary, service method call, and handler invocation.
- All pre-existing test suites continue to pass with zero regressions.
- New automated tests validate scoping behavior and invalid parameter handling.

## Constraints
- Use REQUIREMENTS.md and SPEC.md as the source of truth.
- Keep changes scoped to this task.
- Do not redefine requirements in this file.
