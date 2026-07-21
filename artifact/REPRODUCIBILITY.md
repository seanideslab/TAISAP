# TAISAP Artifact Reproducibility

## Required Metadata

Every generated table or summary must record:

- source commit;
- Docker image digest or equivalent environment lock;
- Python and package versions;
- model IDs and backend snapshots;
- policy version;
- random seeds;
- hardware and region;
- excluded records and exclusion reasons;
- privacy redaction rules;
- exact output checksums.

## Stable Rebuild Interface

Run `make all` from the repository root to rebuild all generated tables once the raw artifact data are available. If GNU Make is unavailable, run `python3 artifact/scripts/run_all.py --target all`; no third-party Python packages are required. Individual public targets are:

```sh
make table_ablation
make table_backends
make table_timing
make table_robustness
make authority_path
make clustered_ci
make fuzz_summary
make load_summary
make audit_agreement
make field_sensitivity
make errsim_ablation
make all
```

Portable no-Make equivalents are:

```sh
python3 artifact/scripts/run_all.py --target validate_artifact
python3 artifact/scripts/run_all.py --target authority_path
python3 artifact/scripts/run_all.py --target all
```

## Evidence Language Constraints

For corpus-bounded fuzzing evidence, use bounded language such as: "No fail-open outcome was observed in the released 500,000-case corpus." Do not claim parser completeness or zero failure probability.

For broker load evidence at C=500, report both safety and degraded service quality: "The system remained fail closed, but service quality degraded and the single-T4 deployment was beyond its sustainable capacity region."

For cross-path timing, if the experiment is not completed, retain the limitation: "Cross-path route inference remains an open timing channel."
