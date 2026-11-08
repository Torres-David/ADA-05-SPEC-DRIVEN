# Change Request

Change ID: CR-02

## Goal
Add an optional `email_domain` filter parameter to the customer search interface (e.g., `'empresa.com'`, `'example.com'`) with format validation, allowing callers to restrict search matches exclusively to customer records belonging to a specified email domain while preserving existing query matching logic, relevance ordering, and complete backward compatibility when omitted.

## Requirements Covered
- FR-04
- FR-06
- AC-04

## Constraints
- Follow AGENTS.md.
- Use REQUIREMENTS.md and SPEC.md as the source of truth.
- Preserve architecture boundaries.
- Do not weaken existing tests.

## Verification
- When `email_domain` is specified (e.g., `'empresa.com'`), only records matching the query whose email belongs to that domain are returned; records matching the search query under different domains are excluded.
- The `email_domain` parameter is normalized: leading `'@'` characters are stripped and matching is case-insensitive (e.g., `'@EMPRESA.COM'` matches `'soporte.ti@empresa.com'`).
- If an invalid `email_domain` is provided (e.g., empty string, strings containing spaces, or strings without a valid domain format such as missing a top-level domain dot), a `ValidationError` is raised, resulting in an HTTP 400 Bad Request response.
- When `email_domain` is `None` or omitted, search matches across all email domains without restriction, maintaining 100% backward compatibility.
- If matches exist for the query in the database but none belong to the specified `email_domain`, `CustomerNotFoundError` is raised, returning an HTTP 404 response with the standard message defined in FR-03.
- The `email_domain` parameter is accepted via dictionary payload (`request_payload['email_domain']`), keyword argument in `CustomerSearchService.search_customers()` / `search()`, and `CustomerSearchHandler.handle()`.
- All 77 pre-existing automated tests continue to pass without regressions.
- New automated tests verify domain-scoped filtering, domain normalization, format validation error handling, and backward compatibility.

## Human Approval
Approved to implement: YES / NO
Approved by: David Torres
Date: 08/11/2026
