# Commands for Generating TAISAP Table Files

Run all commands from the repository root.

## 1. Validate the artifact contract

```sh
make validate_artifact
```

This checks that the schema, manifest template, directories, and documentation stay synchronized.

## 2. Generate one table file

```sh
make authority_path
```

Replace `authority_path` with any public target listed below. Each target writes `artifact/generated_tables/<target>.csv` and records the input files required for that table, their expected paths, presence, row counts, generation time, and source commit.

## 3. Generate all table files

```sh
make all
```

This generates the scaffold table files for every target and then runs full validation.

## Public targets

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
make validate_artifact
make all
```

## Important limitation

The current repository contains a strict scaffold, not the released experiment datasets. The generated CSV files under `artifact/generated_tables/` therefore report table contracts and input availability; they do not fabricate TAISAP experimental statistics. After raw experiment CSVs are populated under `artifact/data/`, rerun the same commands to regenerate the table-status files with nonzero input row counts. Generated CSVs are intentionally ignored by git; commit source data, schemas, and scripts rather than timestamped generated outputs unless a release process explicitly requires checked-in tables.
