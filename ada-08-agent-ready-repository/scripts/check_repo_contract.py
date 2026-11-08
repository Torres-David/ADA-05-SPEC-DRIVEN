#!/usr/bin/env python3
"""
scripts/check_repo_contract.py

Deterministic repository contract & guardrail validator for ADA-08.
Converts critical natural language rules into verifiable, automated gates:
  1. Essential files & directories presence and non-emptiness.
  2. SPEC.md requirement & acceptance criteria traceability (FR-, NFR-, AC-).
  3. AGENTS.md standard commands & contract clauses.
  4. Secret / sensitive token pattern scanner.
  5. Documentation link & file reference integrity (docs/REPO_MAP.md).
  6. Seed database integrity & schema validation (src/customers.json).
  7. Agent adapter contracts (GEMINI.md, CLAUDE.md).
"""

import json
import re
import sys
from pathlib import Path
from typing import List, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent

# 1. Essential files required for repository contract
REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "REQUIREMENTS.md",
    "SPEC.md",
    "ARCHITECTURE.md",
    "TASKS.md",
    "docs/REPO_MAP.md",
    "requirements.txt",
    "src/cli.py",
    "src/handler.py",
    "src/search_services.py",
    "src/customer.py",
    "src/customer_repository.py",
    "src/customers.json",
]

REQUIRED_DIRS = [
    "results",
    "docs",
    "src",
    "test",
    "scripts",
]

# Sensitive patterns that must never be committed
SECRET_PATTERNS = [
    (r"AKIA[0-9A-Z]{16}", "AWS Access Key"),
    (r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----", "Private Key Header"),
    (r"ghp_[0-9a-zA-Z]{36}", "GitHub Personal Access Token"),
    (r"(?:api[_-]?key|secret[_-]?token)\s*=\s*['\"][A-Za-z0-9_\-]{20,}['\"]", "API Key Assignment"),
]


def check_essential_files() -> Tuple[bool, List[str]]:
    failures = []
    for rel_path in REQUIRED_FILES:
        path = ROOT_DIR / rel_path
        if not path.exists():
            failures.append(f"Missing essential file: {rel_path}")
        elif path.stat().st_size == 0:
            failures.append(f"Essential file is empty: {rel_path}")

    for rel_dir in REQUIRED_DIRS:
        dir_path = ROOT_DIR / rel_dir
        if not dir_path.exists() or not dir_path.is_dir():
            failures.append(f"Missing essential directory: {rel_dir}/")

    return len(failures) == 0, failures


def check_spec_traceability() -> Tuple[bool, List[str]]:
    failures = []
    spec_path = ROOT_DIR / "SPEC.md"
    if not spec_path.exists():
        return False, ["SPEC.md does not exist"]

    content = spec_path.read_text(encoding="utf-8")

    # Verify coverage of functional, non-functional, and acceptance criteria IDs
    required_id_patterns = [
        (r"\bFR-01\b", "FR-01"),
        (r"\bFR-06\b", "FR-06"),
        (r"\bNFR-01\b", "NFR-01"),
        (r"\bNFR-02\b", "NFR-02"),
        (r"\bAC-01\b", "AC-01"),
        (r"\bAC-06\b", "AC-06"),
    ]

    for pattern, label in required_id_patterns:
        if not re.search(pattern, content):
            failures.append(f"SPEC.md is missing reference to requirement/criterion ID: {label}")

    return len(failures) == 0, failures


def check_agents_commands() -> Tuple[bool, List[str]]:
    failures = []
    agents_path = ROOT_DIR / "AGENTS.md"
    if not agents_path.exists():
        return False, ["AGENTS.md does not exist"]

    content = agents_path.read_text(encoding="utf-8")

    mandatory_sections = [
        "## Read First",
        "## Sources of Truth",
        "## Standard Commands",
        "Install:",
        "Run:",
        "Test:",
        "Lint:",
        "Verify:",
        "## Change Rules",
        "## Stop Conditions",
        "## Definition of Done",
    ]

    for sec in mandatory_sections:
        if sec not in content:
            failures.append(f"AGENTS.md is missing mandatory section/command: '{sec}'")

    return len(failures) == 0, failures


def check_no_sensitive_secrets() -> Tuple[bool, List[str]]:
    failures = []
    scannable_dirs = [ROOT_DIR / "src", ROOT_DIR / "test", ROOT_DIR / "scripts"]
    files_to_scan: List[Path] = [ROOT_DIR / ".env"]

    for directory in scannable_dirs:
        if directory.exists():
            files_to_scan.extend(directory.rglob("*.py"))

    for file_path in files_to_scan:
        if not file_path.exists():
            continue
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            for pattern, label in SECRET_PATTERNS:
                if re.search(pattern, content, re.IGNORECASE):
                    failures.append(
                        f"Potential secret detected ({label}) in {file_path.relative_to(ROOT_DIR)}"
                    )
        except Exception as exc:
            failures.append(f"Error scanning {file_path.relative_to(ROOT_DIR)}: {exc}")

    return len(failures) == 0, failures


def check_repo_map_link_integrity() -> Tuple[bool, List[str]]:
    failures = []
    repo_map_path = ROOT_DIR / "docs" / "REPO_MAP.md"
    if not repo_map_path.exists():
        return False, ["docs/REPO_MAP.md does not exist"]

    content = repo_map_path.read_text(encoding="utf-8")
    # Extract file paths inside backticks: `src/...`, `test/...`, `REQUIREMENTS.md`, etc.
    referenced_paths = re.findall(r"`([A-Za-z0-9_\-\./\\]+\.[a-zA-Z0-9]+)`", content)

    for ref in referenced_paths:
        target = ROOT_DIR / ref
        if not target.exists():
            failures.append(f"docs/REPO_MAP.md references non-existent path: {ref}")

    return len(failures) == 0, failures


def check_seed_database() -> Tuple[bool, List[str]]:
    failures = []
    data_path = ROOT_DIR / "src" / "customers.json"
    if not data_path.exists():
        return False, ["src/customers.json does not exist"]

    try:
        data = json.loads(data_path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            return False, ["src/customers.json is not a JSON list"]

        if len(data) < 50:
            failures.append(f"Expected >= 50 records in seed data, found {len(data)}")

        expected_keys = {"name", "email"}
        emails = set()
        for idx, item in enumerate(data):
            if set(item.keys()) != expected_keys:
                failures.append(f"Record #{idx} keys mismatch: {set(item.keys())} != {expected_keys}")
                break
            email = item.get("email", "").strip().lower()
            if email in emails:
                failures.append(f"Duplicate email found in seed database: {email}")
                break
            emails.add(email)
    except Exception as exc:
        failures.append(f"Failed parsing src/customers.json: {exc}")

    return len(failures) == 0, failures


def check_agent_adapter_contract() -> Tuple[bool, List[str]]:
    failures = []
    for adapter_file in ["GEMINI.md", "CLAUDE.md"]:
        path = ROOT_DIR / adapter_file
        if path.exists():
            content = path.read_text(encoding="utf-8")
            if "AGENTS.md" not in content or "Do not duplicate project requirements" not in content:
                failures.append(f"{adapter_file} does not delegate cleanly to AGENTS.md")
    return len(failures) == 0, failures


def main() -> int:
    print("=" * 60)
    print("REPO_CONTRACT & GUARDRAIL VALIDATOR (ADA-08)")
    print("=" * 60)

    checks = [
        ("Essential Files & Directories", check_essential_files),
        ("SPEC.md Requirement Traceability", check_spec_traceability),
        ("AGENTS.md Standard Commands & Contract", check_agents_commands),
        ("Secret & Sensitive Pattern Scanner", check_no_sensitive_secrets),
        ("Documentation Link Integrity", check_repo_map_link_integrity),
        ("Seed Database Integrity", check_seed_database),
        ("Agent Adapter Contracts", check_agent_adapter_contract),
    ]

    all_passed = True
    for name, check_fn in checks:
        passed, failures = check_fn()
        if passed:
            print(f"  [PASS] {name}")
        else:
            print(f"  [FAIL] {name}")
            for msg in failures:
                print(f"         -> {msg}")
            all_passed = False

    print("=" * 60)
    if all_passed:
        print("REPO_CONTRACT: ALL GUARDRAILS PASSED (PASS)")
        return 0
    else:
        print("REPO_CONTRACT: GUARDRAIL VIOLATIONS DETECTED (FAIL)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
