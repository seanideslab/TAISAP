.PHONY: table_ablation table_backends table_timing table_robustness authority_path clustered_ci fuzz_summary load_summary audit_agreement field_sensitivity validate_artifact all

VALIDATE_ARTIFACT := PYTHONDONTWRITEBYTECODE=1 python3 artifact/scripts/validate_artifact.py
GENERATE_TABLE := PYTHONDONTWRITEBYTECODE=1 python3 artifact/scripts/generate_table_files.py

table_ablation:
	$(GENERATE_TABLE) --target $@

table_backends:
	$(GENERATE_TABLE) --target $@

table_timing:
	$(GENERATE_TABLE) --target $@

table_robustness:
	$(GENERATE_TABLE) --target $@

authority_path:
	$(GENERATE_TABLE) --target $@

clustered_ci:
	$(GENERATE_TABLE) --target $@

fuzz_summary:
	$(GENERATE_TABLE) --target $@

load_summary:
	$(GENERATE_TABLE) --target $@

audit_agreement:
	$(GENERATE_TABLE) --target $@

field_sensitivity:
	$(GENERATE_TABLE) --target $@

validate_artifact:
	$(VALIDATE_ARTIFACT) --target all

all: table_ablation table_backends table_timing table_robustness authority_path clustered_ci fuzz_summary load_summary audit_agreement field_sensitivity validate_artifact
