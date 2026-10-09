---
name: reviewing-pull-requests
description: |
    Reviews a Pull Request for engineering readiness using repository
    requirements/specification, code changes and test evidence.
    Use when the user asks to review a PR, assess PR readiness,
    check a pull request against requirements, or produce a review report.
    Do NOT use to implement issues, modify code, comment on GitHub,
    approve PRs, merge PRs, or explain generic Git concepts.
version: 1.0.1
metadata:
    owner: Josue David Torres Tec
    course: UADY-IS-AI
---

# Reviewing Pull Requests
## When to use
Use this skill for PR readiness reviews before human approval.
## Preconditions
- Repository / PR is accessible.
- Read-only inspection is sufficient.
- If REQUIREMENTS.md or SPEC.md exists, use it as normative context.
## Workflow
1. Identify the PR / branch / diff to review. Isolate analysis strictly to the PR changeset; do not inspect uncommitted local working tree changes or browse unrelated project directories.
2. Read project-level instructions and relevant requirements/specification.
3. Inspect changed files belonging strictly to the PR diff and map them to the requested behavior.
4. Inspect or run relevant tests.
5. Apply `references/review_checklist.md`.
6. Classify findings using `references/severity_guide.md`.
7. Create a draft report using `assets/review_report_template.md`.
8. Run `scripts/validate_review_report.py` on the report.
9. If validation fails, repair the report and validate again.
10. Stop and present the report to the human reviewer.
## Safety / Boundaries
- Read-only review of GitHub/repository content.
- Do not modify production code unless explicitly starting a new task.
- Do not comment, approve or merge Pull Requests.
- Do not weaken tests to remove findings.
- Stop if REQUIREMENTS.md and SPEC.md conflict.
- Scope isolation: Do not inspect uncommitted local working copy changes or explore unrelated directories when reviewing a remote PR. Confine inspection strictly to the PR diff, normative specifications, and relevant test execution.
## Output
Create:
results/pr-readiness-review.md
The report must distinguish:
- MUST FIX
- SHOULD FIX
- OPTIONAL
- Human decision required
