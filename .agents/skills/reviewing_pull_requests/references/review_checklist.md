# PR Review Checklist
## Requirements / Specification
- Changed behavior maps to an existing Requirement / Acceptance Criterion.
- No undocumented business rule is introduced.
- SPEC and implementation are consistent.
## Code
- Change is focused and understandable.
- Error handling is appropriate.
- No unrelated refactoring is mixed into the PR.
- Dependencies are justified.
## Tests
- New behavior has automated evidence.
- Important edge cases are covered.
- Existing behavior is not weakened.
- Tests verify behavior, not only implementation details.
## Architecture
- Change respects documented boundaries.
- ARCHITECTURE.md is updated if the design changed.
## Security
- No secrets or credentials.
- No unnecessary permissions.
- External input is validated where required.
## Evidence
- Findings cite file/test/requirement evidence.
