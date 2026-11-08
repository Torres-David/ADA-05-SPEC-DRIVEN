# AGENTS.md
ADA-08 · Agent-Ready Repository · Ingeniería de Software asistida por IA

## Read First
1. REQUIREMENTS.md
2. SPEC.md
3. ARCHITECTURE.md
4. TASKS.md
5. docs/REPO_MAP.md

## Sources of Truth
- Requirements live only in REQUIREMENTS.md.
- Verifiable behavior lives in SPEC.md.
- Architectural boundaries live in ARCHITECTURE.md.
- Active change scope lives in TASK_UNDER_TEST.md (precedes TASKS.md when present).
- Do not change requirements/spec merely to make tests pass.

## Repository Map
- src/        implementation
- test/       automated tests
- docs/       architecture and operational context
- scripts/    deterministic checks
- results/    generated evidence

## Standard Commands
Install: python -m pip install -e . (or pip install pytest)
Run: python src/cli.py "<query>"
Test: pytest
Lint: python -m compileall src test scripts
Verify: ./scripts/verify_repo.sh (or python scripts/verify_repo.py)

## Change Rules
- Keep changes scoped to the requested task.
- Do not weaken or delete existing tests.
- Do not introduce new dependencies without justification.
- Do not modify secrets (.env) or protected specification files (REQUIREMENTS.md, SPEC.md).
- Preserve file line endings (CRLF/LF) and do not run unauthorized git state/history commands.

## Stop Conditions
Stop and ask for human input when:
- requirements conflict,
- a destructive action is required,
- an architecture boundary must change,
- a required external system is unavailable.

## Definition of Done
- Relevant tests pass (`pytest`).
- Acceptance criteria are covered and verified.
- No unrelated or protected files are changed.
- Documentation reflects final behavior.
