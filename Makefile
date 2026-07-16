.PHONY: table_ablation table_backends table_timing table_robustness authority_path clustered_ci fuzz_summary load_summary audit_agreement field_sensitivity validate_artifact all

VALIDATE_ARTIFACT := python3 artifact/scripts/validate_artifact.py

table_ablation:
	$(VALIDATE_ARTIFACT) --target $@

table_backends:
	$(VALIDATE_ARTIFACT) --target $@

table_timing:
	$(VALIDATE_ARTIFACT) --target $@

table_robustness:
	$(VALIDATE_ARTIFACT) --target $@

authority_path:
	$(VALIDATE_ARTIFACT) --target $@

clustered_ci:
	$(VALIDATE_ARTIFACT) --target $@

fuzz_summary:
	$(VALIDATE_ARTIFACT) --target $@

load_summary:
	$(VALIDATE_ARTIFACT) --target $@

audit_agreement:
	$(VALIDATE_ARTIFACT) --target $@

field_sensitivity:
	$(VALIDATE_ARTIFACT) --target $@

validate_artifact:
	$(VALIDATE_ARTIFACT) --target all

all: table_ablation table_backends table_timing table_robustness authority_path clustered_ci fuzz_summary load_summary audit_agreement field_sensitivity validate_artifact
