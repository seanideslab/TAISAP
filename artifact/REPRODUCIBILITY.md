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

Run `make all` from the repository root to rebuild all generated tables once the raw artifact data are available. Individual public targets are:

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
make all
```

## Evidence Language Constraints

For corpus-bounded fuzzing evidence, use bounded language such as: "No fail-open outcome was observed in the released 500,000-case corpus." Do not claim parser completeness or zero failure probability.

For broker load evidence at C=500, report both safety and degraded service quality: "The system remained fail closed, but service quality degraded and the single-T4 deployment was beyond its sustainable capacity region."

For cross-path timing, if the experiment is not completed, retain the limitation: "Cross-path route inference remains an open timing channel."
