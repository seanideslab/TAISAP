#!/usr/bin/env python3
"""Generate TAISAP scaffold table files from the artifact schema.

This script intentionally does not fabricate experimental statistics. Until raw
experiment CSVs are released under `artifact/data/`, each generated table records
its required inputs, whether those inputs are present, and the artifact contract
that downstream analysis scripts must satisfy.
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from validate_artifact import TARGETS, validate_scaffold

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "artifact" / "configs" / "artifact_schema.json"
GENERATED_TABLES_DIR = REPO_ROOT / "artifact" / "generated_tables"

DATA_LOCATIONS = {
    "ablation_sessions.csv": "artifact/data/ablation/ablation_sessions.csv",
    "ablation_turns.csv": "artifact/data/ablation/ablation_turns.csv",
    "adversarial_probes.csv": "artifact/data/ablation/adversarial_probes.csv",
    "authority_path_decomposition.csv": "artifact/data/authority_path/authority_path_decomposition.csv",
    "parser_fuzz_cases.csv": "artifact/data/fuzzing/parser_fuzz_cases.csv",
    "parser_fuzz_campaigns.csv": "artifact/data/fuzzing/parser_fuzz_campaigns.csv",
    "broker_load_runs.csv": "artifact/data/broker_load/broker_load_runs.csv",
    "backend_probe_results.csv": "artifact/data/backends/backend_probe_results.csv",
    "backend_session_results.csv": "artifact/data/backends/backend_session_results.csv",
    "backend_paired_comparisons.csv": "artifact/data/backends/backend_paired_comparisons.csv",
    "timing_sequence_manifest.csv": "artifact/data/timing/timing_sequence_manifest.csv",
    "timing_predictions.csv": "artifact/data/timing/timing_predictions.csv",
    "timing_paired_delta_auc.csv": "artifact/data/timing/timing_paired_delta_auc.csv",
    "containment_cases.csv": "artifact/data/ablation/containment_cases.csv",
    "state_poisoning_cases.csv": "artifact/data/ablation/state_poisoning_cases.csv",
    "benign_commands.csv": "artifact/data/ablation/benign_commands.csv",
    "human_audit_labels.csv": "artifact/data/human_audit/human_audit_labels.csv",
    "field_filtering_sensitivity.csv": "artifact/data/field_sensitivity/field_filtering_sensitivity.csv",
    "artifact_manifest.json": "artifact/artifact_manifest.json",
    "DATA_DICTIONARY.md": "artifact/DATA_DICTIONARY.md",
    "REPRODUCIBILITY.md": "artifact/REPRODUCIBILITY.md",
}


def git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def row_count(path: Path) -> int:
    if not path.exists() or not path.is_file():
        return 0
    if path.suffix.lower() != ".csv":
        return 1
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        rows = list(reader)
    return max(len(rows) - 1, 0)


def inputs_for_target(target: str, schema: dict) -> list[str]:
    if target == "all":
        return list(schema["required_release_files"])
    if target == "validate_artifact":
        return ["artifact_manifest.json", "DATA_DICTIONARY.md", "REPRODUCIBILITY.md"]
    return list(TARGETS[target])


def write_target_table(target: str, inputs: list[str]) -> Path:
    GENERATED_TABLES_DIR.mkdir(parents=True, exist_ok=True)
    output_path = GENERATED_TABLES_DIR / f"{target}.csv"
    generated_at = datetime.now(timezone.utc).isoformat()
    commit = git_commit()

    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "target",
                "required_file",
                "expected_path",
                "exists",
                "row_count",
                "generated_at",
                "source_commit",
            ],
        )
        writer.writeheader()
        for required_file in inputs:
            expected_path = DATA_LOCATIONS.get(required_file, required_file)
            absolute_path = REPO_ROOT / expected_path
            writer.writerow(
                {
                    "target": target,
                    "required_file": required_file,
                    "expected_path": expected_path,
                    "exists": absolute_path.exists(),
                    "row_count": row_count(absolute_path),
                    "generated_at": generated_at,
                    "source_commit": commit,
                }
            )
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target",
        required=True,
        choices=sorted(["all", "validate_artifact", *TARGETS]),
        help="Table target to generate.",
    )
    args = parser.parse_args()

    validation_target = "all" if args.target == "validate_artifact" else args.target
    errors = validate_scaffold(validation_target)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    output_path = write_target_table(args.target, inputs_for_target(args.target, schema))
    print(f"Generated {output_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
