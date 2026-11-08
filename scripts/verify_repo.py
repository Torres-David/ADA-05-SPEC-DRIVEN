#!/usr/bin/env python3
"""
scripts/verify_repo.py

Deterministic repository verification script for ADA-08.
Executes the minimum mandatory verification pipeline:
  [1/3] Running tests (pytest -q)
  [2/3] Running lint (compileall -q)
  [3/3] Repository checks (check_repo_contract.py)
"""

import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent


def run_command(label: str, cmd: list) -> bool:
    print(f"\n{label}")
    result = subprocess.run(cmd, cwd=str(ROOT_DIR))
    if result.returncode != 0:
        print(f"VERIFY_REPO: FAIL ({label})")
        return False
    return True


def main() -> int:
    steps = [
        ("[1/3] Running tests", [sys.executable, "-m", "pytest", "-q"]),
        ("[2/3] Running lint", [sys.executable, "-m", "compileall", "-q", "src", "test", "scripts"]),
        ("[3/3] Repository checks", [sys.executable, "scripts/check_repo_contract.py"]),
    ]

    for label, cmd in steps:
        if not run_command(label, cmd):
            return 1

    print("\nVERIFY_REPO: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
