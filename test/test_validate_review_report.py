"""
test/test_validate_review_report.py

Pruebas unitarias para scripts/validate_review_report.py
"""

from pathlib import Path
import pytest
from scripts.validate_review_report import (
    REQUIRED_SECTIONS,
    main,
    validate_review_report,
)


@pytest.fixture
def sample_valid_report(tmp_path: Path) -> Path:
    report_file = tmp_path / "valid_report.md"
    content = """# PR Readiness Review
## Review Context
PR / Branch: Cambio-ADA-06-final -> main
Reviewer Agent: Antigravity
Date: 2026-10-08

## Requirements / Acceptance Criteria Reviewed
- FR-01, FR-02, FR-03, FR-04, FR-05, FR-06
- AC-01 a AC-06
- T-07

## Test Evidence
- 47 tests passed in 0.10s via pytest.

## MUST FIX
None.

## SHOULD FIX
- Inconsistencia menor en HTTP 429.

## OPTIONAL
- Refactorización de ordenamiento compuesto.

## Final Review Summary
MUST FIX count: 0
SHOULD FIX count: 1
OPTIONAL count: 1
Human decision required: YES
"""
    report_file.write_text(content, encoding="utf-8")
    return report_file


def test_validate_review_report_success(sample_valid_report: Path):
    is_valid, passed, failed = validate_review_report(sample_valid_report)
    assert is_valid is True
    assert len(failed) == 0
    assert len(passed) == len(REQUIRED_SECTIONS) + 1  # file exists + all sections


def test_validate_review_report_file_not_found(tmp_path: Path):
    missing_file = tmp_path / "does_not_exist.md"
    is_valid, passed, failed = validate_review_report(missing_file)
    assert is_valid is False
    assert any("no existe" in err for err in failed)


def test_validate_review_report_path_is_directory(tmp_path: Path):
    is_valid, passed, failed = validate_review_report(tmp_path)
    assert is_valid is False
    assert any("no es un archivo válido" in err for err in failed)


@pytest.mark.parametrize(
    "missing_section_text,section_id",
    [
        ("## Review Context", "review_context"),
        ("## Requirements / Acceptance Criteria Reviewed", "requirements_reviewed"),
        ("## Test Evidence", "test_evidence"),
        ("## MUST FIX", "must_fix"),
        ("## SHOULD FIX", "should_fix"),
        ("## OPTIONAL", "optional"),
        ("## Final Review Summary", "final_summary"),
        ("Human decision required:", "human_decision"),
    ],
)
def test_validate_review_report_missing_individual_sections(
    sample_valid_report: Path, tmp_path: Path, missing_section_text: str, section_id: str
):
    original_content = sample_valid_report.read_text(encoding="utf-8")
    modified_content = original_content.replace(missing_section_text, "")

    broken_file = tmp_path / f"broken_{section_id}.md"
    broken_file.write_text(modified_content, encoding="utf-8")

    is_valid, passed, failed = validate_review_report(broken_file)
    assert is_valid is False
    assert len(failed) >= 1


def test_main_cli_success(sample_valid_report: Path):
    exit_code = main([str(sample_valid_report)])
    assert exit_code == 0


def test_main_cli_missing_file(tmp_path: Path):
    missing_file = tmp_path / "ghost.md"
    exit_code = main([str(missing_file)])
    assert exit_code == 1


def test_main_cli_no_args_without_default(monkeypatch, tmp_path: Path):
    # Asegurar que no encuentre default_candidate
    monkeypatch.chdir(tmp_path)
    exit_code = main([])
    assert exit_code == 1
