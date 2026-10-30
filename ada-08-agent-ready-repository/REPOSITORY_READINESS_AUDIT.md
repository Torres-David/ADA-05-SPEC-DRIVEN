# Repository Readiness Audit

## BEFORE

| Dimension | Score 0-5 | Weighted | Evidence | Main Gap |
|---|---:|---:|---|---|
| Entry Point & Navigation | 3 | 9.0 / 15 | `README.md` describes the project purpose, architecture, and CLI usage; `AGENTS.md` indexes key source-of-truth files (`REQUIREMENTS.md`, `SPEC.md`, `ARCHITECTURE.md`, `TASKS.md`). | Lacks a centralized navigation map; dynamic change specifications (`TASK_UNDER_TEST.md`) required manual discovery via prompt. |
| Agent Instructions | 3 | 9.0 / 15 | `AGENTS.md` provides clear project rules, source-of-truth hierarchy, read order, and an explicit Definition of Done. | Omits operational tool boundaries (e.g. prohibited git inspection commands), deliverable report schemas, and OS/CRLF line-ending conventions. |
| Build / Run / Test | 3 | 9.0 / 15 | `pytest.ini` configures `pythonpath = . src`; `pytest` runs 60+ tests out of the box with zero manual environment configuration. | No formal dependency manifest (`pyproject.toml` or `requirements.txt`); lacks a unified repository verification script. |
| Architecture Boundaries | 3 | 6.0 / 10 | `ARCHITECTURE.md` details layers (Handler, Services, Domain, Repository), responsibilities, and data flow; `SPEC.md` defines out-of-scope aspects. | Lacks negative architectural boundaries (explicit list of what NOT to touch); no static import or layer boundary enforcement tooling. |
| Requirements & Traceability | 4 | 8.0 / 10 | Requirements (`FR-01` to `FR-06`, `NFR-01` to `NFR-03`), acceptance criteria (`AC-01` to `AC-06`), and tasks (`T-01` to `T-08`) use traceable IDs in tests. | Minor language inconsistency across requirements (some FR in English, some in Spanish); traceability verification is manual rather than automated. |
| Automation & Guardrails | 1 | 2.0 / 10 | A PR report validator script exists (`scripts/validate_review_report.py`). | Total absence of CI workflows (`.github/workflows`), pre-commit hooks, linters (ruff/flake8), or automated checks enforcing `AGENTS.md` rules. |
| Testability & Evidence | 4 | 12.0 / 15 | Fast automated test suite (69 tests in 0.2s) covering domain entities, seed data integrity, acceptance criteria, NFR latency, and rate limiting. | No automated test coverage measurement (`pytest-cov`); evidence collection and report generation rely on manual agent steps. |
| Safety & Permissions | 2 | 4.0 / 10 | `FR-05`/`AC-05` protect sensitive fields in customer DTOs; `NFR-02` prevents abuse via sliding-window rate limiting. | No operational safety boundaries for agents (unrestricted git commands triggered user permission prompts); lacks a formal root `.gitignore`. |

**TOTAL BEFORE: 59.0 / 100**

### Top 3 Friction Points:
1. **Lack of active automation and guardrails (Score: 1/5)**: Constraints in `AGENTS.md` ("do not modify SPEC.md", "do not weaken tests", "no unrelated files modified") rely solely on prompt adherence with no automated linters, pre-commit hooks, or CI checks to enforce them deterministically.
2. **Undeclared operational boundaries and environment constraints (Score: 2/5)**: Missing explicit tool boundaries (e.g., git command restrictions) and undeclared Windows CRLF (`\r\n`) vs Unix LF (`\n`) line terminators caused string-replacement tool failures and user permission interruptions.
3. **Missing dependency manifest and unified verification entry point (Score: 3/5)**: The repository lacks a standard `pyproject.toml` or `requirements.txt` with pinned versions and lacks a single-command verification script (e.g., `verify.py` or `check.sh`) to run tests, linters, and repository integrity checks in one step.

---

# Implicit Knowledge Found

## IK-01
**What:**  
Source files on Windows repositories use CRLF (`\r\n`) line endings, which causes exact multiline string replacement tools (`edit_file`) expecting Unix LF (`\n`) to fail silently or report missing targets.  
**How was it discovered:**  
An `edit_file` tool call failed on `src/search_services.py`, confirmed by inspecting raw file bytes with Python (`open('src/search_services.py', 'rb').read()`).  
**Should this remain implicit?**  
NO  
**Where should it become explicit?**  
In a root `.gitattributes` file enforcing `* text=auto eol=lf`, and documented under environment guidelines in `AGENTS.md`.  
**Remediation:**  
Create `.gitattributes` to normalize line endings across platforms deterministically.

## IK-02
**What:**  
Git status and history inspection commands are out of scope and should not be invoked by agents during standard change execution.  
**How was it discovered:**  
A permission denial and explicit user intervention: *"No revisar git status ni nada de git si no es parte del alcance de lo indicado"*.  
**Should this remain implicit?**  
NO  
**Where should it become explicit?**  
`AGENTS.md` under an explicit "Tool & Operational Constraints" section.  
**Risk:**  
Agents waste context, prompt users unnecessarily for permissions, or perform unauthorized repository inspections.  
**Remediation:**  
Add an explicit rule in `AGENTS.md`: "Do not execute git inspection or state commands unless explicitly requested by the user".

## IK-03
**What:**  
Transient task-under-test specifications (`TASK_UNDER_TEST.md` / `CR-01`) take precedence for the specific change scope, but `AGENTS.md` only instructed agents to "Follow TASKS.md" without defining how `TASK_UNDER_TEST.md` integrates into the workflow.  
**How was it discovered:**  
The user prompt explicitly referenced `TASK_UNDER_TEST.md`, whereas root documentation files did not link to it.  
**Should this remain implicit?**  
NO  
**Where should it become explicit?**  
`AGENTS.md` and `TASKS.md`.  
**Risk:**  
Autonomous agents starting from `AGENTS.md` alone would only inspect `TASKS.md` and miss change request verification criteria defined in `TASK_UNDER_TEST.md`.  
**Remediation:**  
Define the document precedence order in `AGENTS.md` (`TASK_UNDER_TEST.md` > `TASKS.md` for active change requests).

## IK-04
**What:**  
The test framework (`pytest`) is assumed to exist in the global/ambient Python environment, but there is no declarative package specification (`pyproject.toml` or `requirements.txt`) to bootstrap a clean environment or CI runner.  
**How was it discovered:**  
Inspecting the repository root for dependency manifests and finding none.  
**Should this remain implicit?**  
NO  
**Where should it become explicit?**  
`pyproject.toml` or `requirements-dev.txt`.  
**Risk:**  
Clean checkouts, containers, or CI environments will fail immediately without clear guidance on required packages and versions.  
**Remediation:**  
Provide a declarative `pyproject.toml` specifying project dependencies (`pytest>=8.0`) and tool configurations.
