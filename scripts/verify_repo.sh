#!/usr/bin/env bash
set -euo pipefail

echo "[1/3] Running tests"
pytest -q

echo "[2/3] Running lint"
python -m compileall -q src test scripts

echo "[3/3] Repository checks"
python scripts/check_repo_contract.py

echo "VERIFY_REPO: PASS"
