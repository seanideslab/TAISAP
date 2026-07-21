#!/usr/bin/env python3
"""Validate the TAISAP artifact scaffold and manifest contract.

The repository currently contains a scaffold rather than released experiment data.
This validator makes the scaffold strict: it checks that the documented public
interface, artifact directories, manifest schema, and manifest entries stay in
sync before real generation scripts are added.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "artifact" / "configs" / "artifact_schema.json"
MANIFEST_PATH = REPO_ROOT / "artifact" / "artifact_manifest.json"
PLAN_PATH = REPO_ROOT / "docs" / "taisap_evidence_execution_plan.md"
DATA_DICTIONARY_PATH = REPO_ROOT / "artifact" / "DATA_DICTIONARY.md"
REPRODUCIBILITY_PATH = REPO_ROOT / "artifact" / "REPRODUCIBILITY.md"

TARGETS = {
    "table_ablation": [
        "baseline_ablation_results.csv",
        "prompt_injection_expanded_results.csv",
    ],
    "table_backends": ["model_generalization_results.csv"],
    "table_timing": ["timing_sequence_results.csv"],
    "table_robustness": [
        "containment_stress_results.csv",
        "svl_state_poisoning_results.csv",
        "benign_false_positive_results.csv",
    ],
    "authority_path": ["authority_path_decomposition.csv"],
    "clustered_ci": [
        "baseline_ablation_results.csv",
        "prompt_injection_expanded_results.csv",
    ],
    "fuzz_summary": ["parser_fuzz_results.csv"],
    "load_summary": ["broker_load_results.csv"],
    "audit_agreement": ["human_audit_labels.csv"],
    "field_sensitivity": ["field_filtering_sensitivity.csv"],
    "errsim_ablation": ["errsim_ablation_results.csv"],
}


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path} is not valid JSON: {exc}") from exc


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def require_text_contains(path: Path, snippets: Iterable[str], errors: list[str]) -> None:
    require(path.exists(), f"Missing required document: {path.relative_to(REPO_ROOT)}", errors)
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    for snippet in snippets:
        require(
            snippet in text,
            f"{path.relative_to(REPO_ROOT)} does not document `{snippet}`",
            errors,
        )


def validate_scaffold(scope: str) -> list[str]:
    errors: list[str] = []
    schema = load_json(SCHEMA_PATH)

    required_release_files = schema["required_release_files"]
    scoped_release_files = TARGETS.get(scope, required_release_files)

    for directory in schema["artifact_directories"]:
        require(
            (REPO_ROOT / directory).is_dir(),
            f"Missing artifact directory: {directory}",
            errors,
        )

    require_text_contains(PLAN_PATH, scoped_release_files, errors)
    require_text_contains(DATA_DICTIONARY_PATH, ["source_commit", "policy_version"], errors)
    require_text_contains(REPRODUCIBILITY_PATH, ["make all", "source commit"], errors)

    manifest = load_json(MANIFEST_PATH)
    require(
        manifest.get("schema_version") == schema["schema_version"],
        "artifact_manifest.json schema_version does not match artifact_schema.json",
        errors,
    )
    require(isinstance(manifest.get("files"), list), "manifest `files` must be a list", errors)

    manifest_fields = set(schema["manifest_required_fields"])
    for index, entry in enumerate(manifest.get("files", [])):
        require(isinstance(entry, dict), f"manifest files[{index}] must be an object", errors)
        if not isinstance(entry, dict):
            continue
        missing = sorted(manifest_fields - set(entry))
        require(not missing, f"manifest files[{index}] is missing fields: {missing}", errors)

    require_text_contains(
        DATA_DICTIONARY_PATH,
        schema["authority_path_columns"] + schema["allowed_root_causes"],
        errors,
    )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target",
        default="all",
        choices=sorted(["all", *TARGETS]),
        help="Limit validation to the files documented for one public Make target.",
    )
    args = parser.parse_args()

    errors = validate_scaffold(args.target)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Validated TAISAP artifact scaffold for target: {args.target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
