#!/usr/bin/env python3
"""
scripts/validate_review_report.py

Validador determinista de reportes de revisión de Pull Requests (PR Readiness Review).
Verifica la estructura y presencia de secciones obligatorias sin juzgar la calidad del código.
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Definición de las comprobaciones deterministas requeridas
REQUIRED_SECTIONS: List[Dict[str, str]] = [
    {
        "id": "review_context",
        "name": "Review Context",
        "description": "Sección 'Review Context'",
        "pattern": r"(?m)^(?:#{1,6}\s+|\*\*)Review Context\b.*$|^(?:\s*)Review Context\s*$",
    },
    {
        "id": "requirements_reviewed",
        "name": "Requirements / Acceptance Criteria Reviewed",
        "description": "Sección 'Requirements / Acceptance Criteria Reviewed'",
        "pattern": r"(?m)^(?:#{1,6}\s+|\*\*)Requirements\s*/\s*Acceptance Criteria Reviewed\b.*$|^(?:\s*)Requirements\s*/\s*Acceptance Criteria Reviewed\s*$",
    },
    {
        "id": "test_evidence",
        "name": "Test Evidence",
        "description": "Sección 'Test Evidence'",
        "pattern": r"(?m)^(?:#{1,6}\s+|\*\*)Test Evidence\b.*$|^(?:\s*)Test Evidence\s*$",
    },
    {
        "id": "must_fix",
        "name": "MUST FIX",
        "description": "Sección 'MUST FIX'",
        "pattern": r"(?m)^(?:#{1,6}\s+|\*\*)MUST FIX\b.*$|^(?:\s*)MUST FIX\s*$",
    },
    {
        "id": "should_fix",
        "name": "SHOULD FIX",
        "description": "Sección 'SHOULD FIX'",
        "pattern": r"(?m)^(?:#{1,6}\s+|\*\*)SHOULD FIX\b.*$|^(?:\s*)SHOULD FIX\s*$",
    },
    {
        "id": "optional",
        "name": "OPTIONAL",
        "description": "Sección 'OPTIONAL'",
        "pattern": r"(?m)^(?:#{1,6}\s+|\*\*)OPTIONAL\b.*$|^(?:\s*)OPTIONAL\s*$",
    },
    {
        "id": "final_summary",
        "name": "Final Review Summary",
        "description": "Sección 'Final Review Summary'",
        "pattern": r"(?m)^(?:#{1,6}\s+|\*\*)Final Review Summary\b.*$|^(?:\s*)Final Review Summary\s*$",
    },
    {
        "id": "human_decision",
        "name": "Human decision required",
        "description": "Línea 'Human decision required'",
        "pattern": r"(?m)^.*Human\s+decision\s+required.*$",
    },
]


def validate_review_report(report_path: Path) -> Tuple[bool, List[str], List[str]]:
    """
    Valida los aspectos deterministas del archivo de reporte.

    Retorna:
        Tuple[bool, List[str], List[str]]:
            - bool: True si todas las comprobaciones son exitosas, False en caso contrario.
            - List[str]: Lista de verificaciones superadas ([PASS]).
            - List[str]: Lista de verificaciones fallidas ([FAIL]).
    """
    passed: List[str] = []
    failed: List[str] = []

    # 1. Comprobación de existencia del archivo
    if not report_path.exists():
        failed.append(f"El archivo no existe: '{report_path}'")
        return False, passed, failed

    if not report_path.is_file():
        failed.append(f"La ruta especificada no es un archivo válido: '{report_path}'")
        return False, passed, failed

    passed.append(f"El archivo existe: '{report_path}'")

    # Lectura del contenido
    try:
        content = report_path.read_text(encoding="utf-8")
    except Exception as exc:
        failed.append(f"No se pudo leer el archivo '{report_path}': {exc}")
        return False, passed, failed

    # 2. Comprobación de secciones y líneas obligatorias
    for section in REQUIRED_SECTIONS:
        match = re.search(section["pattern"], content, re.IGNORECASE)
        if match:
            passed.append(f"Incluye {section['description']}")
        else:
            failed.append(f"Falta la {section['description']}")

    is_valid = len(failed) == 0
    return is_valid, passed, failed


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validador determinista de reportes de revisión de Pull Requests (PR Readiness Review)."
    )
    parser.add_argument(
        "report_path",
        nargs="?",
        default=None,
        help="Ruta al archivo de reporte markdown a validar (ej: results/pr-readiness-review.md).",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    if not args.report_path:
        default_candidate = Path("results/pr-readiness-review.md")
        if default_candidate.exists():
            report_path = default_candidate
        else:
            print("ERROR: Debe especificar la ruta del archivo de reporte a validar.", file=sys.stderr)
            print("Uso: python scripts/validate_review_report.py <ruta_al_reporte.md>", file=sys.stderr)
            return 1
    else:
        report_path = Path(args.report_path)

    print("=" * 70)
    print(" VALIDACIÓN DETERMINISTA DE REPORTE DE REVISIÓN")
    print(f" Objetivo: {report_path}")
    print("=" * 70)

    is_valid, passed, failed = validate_review_report(report_path)

    for item in passed:
        print(f" [PASS] {item}")

    for item in failed:
        print(f" [FAIL] {item}")

    print("-" * 70)
    if is_valid:
        print(" RESULTADO: VÁLIDO (Exit Code 0)")
        print(" Todas las secciones y directivas deterministas están presentes.")
        print("=" * 70)
        return 0
    else:
        print(f" RESULTADO: INVÁLIDO (Exit Code 1) - {len(failed)} verificación(es) fallida(s).")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    sys.exit(main())
