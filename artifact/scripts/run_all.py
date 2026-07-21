#!/usr/bin/env python3
"""Run TAISAP artifact generation/validation without requiring `make`.

This is the portable entry point for environments that have Python 3 but do not
have GNU Make installed. It uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from validate_artifact import TARGETS

REPO_ROOT = Path(__file__).resolve().parents[2]
GENERATOR = REPO_ROOT / "artifact" / "scripts" / "generate_table_files.py"
VALIDATOR = REPO_ROOT / "artifact" / "scripts" / "validate_artifact.py"
ORDERED_TARGETS = [
    "table_ablation",
    "table_backends",
    "table_timing",
    "table_robustness",
    "authority_path",
    "clustered_ci",
    "fuzz_summary",
    "load_summary",
    "audit_agreement",
    "field_sensitivity",
    "errsim_ablation",
]


def run(command: list[str]) -> None:
    print("+ " + " ".join(command))
    subprocess.run(command, cwd=REPO_ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target",
        choices=sorted(["all", "validate_artifact", *TARGETS]),
        default="all",
        help="Target to run without make. Defaults to all.",
    )
    args = parser.parse_args()

    python = sys.executable
    if args.target == "validate_artifact":
        run([python, str(VALIDATOR.relative_to(REPO_ROOT)), "--target", "all"])
        return 0

    if args.target == "all":
        for target in ORDERED_TARGETS:
            run([python, str(GENERATOR.relative_to(REPO_ROOT)), "--target", target])
        run([python, str(VALIDATOR.relative_to(REPO_ROOT)), "--target", "all"])
        return 0

    run([python, str(GENERATOR.relative_to(REPO_ROOT)), "--target", args.target])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
