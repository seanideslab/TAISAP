# TAISAP Post-Submission Evidence Execution Plan

This plan tracks the remaining P0 evidence and P1 strengthening experiments for *Bounding Untrusted LLMs in Interactive Honeypots: Deterministic Mediation, Transactional State Verification, and Timing-Fingerprint Mitigation*.

## Principles

- Every new numeric result must be rebuildable from the released artifact.
- The main manuscript should keep only results that directly answer RQ1--RQ4.
- Detailed diagnostics, robustness checks, and raw/aggregate sufficient statistics belong in the appendix or repository.
- P1-3, the structured-output attack benchmark, is intentionally out of scope and will be planned separately.

## Priority Overview

| Priority | Work item | Primary question | New experiment required? |
|---|---|---|---:|
| P0-1 | B3 residual 28 ASR authority-path decomposition | Did failures expand execution/state/egress authority? | Maybe trace-only |
| P0-2 | Cluster-adjusted statistics for five configurations | What are uncertainty and effect sizes for B3 vs. baselines? | Usually recompute |
| P0-3 | Parser fuzz corpus, coverage, campaign metadata | Is the 500,000-case claim reproducible and coverage-bounded? | Maybe coverage rerun |
| P0-4 | Broker load repeated runs | Does C=500 fail closed under degraded service quality? | Recommended |
| P0-5 | Four-backend failure profile and paired analysis | Does the boundary hold across the four evaluated backends? | Usually recompute/summarize |
| P0-6 | Timing paired delta AUC and cross-path attack | What is the direct HMM effect and remaining dual-path leakage? | Delta AUC recompute; cross-path new |
| P0-7 | Human audit multi-rater statistics | Are PCS/ICA/ASR labels reliable? | Usually recompute |
| P0-8 | Artifact, data dictionary, rebuild scripts | Can all tables and CIs be regenerated? | Organize/rebuild |
| P1-1 | GreyNoise/field-cohort sensitivity | Are field findings threshold-driven? | Usually recompute |
| P1-2 | ERRSIM vs. hard refusal | Does ERRSIM reduce policy disclosure/detection? | New small experiment |

## P0 Completion Checklist

- [ ] P0-1: `authority_path_decomposition.csv` and generator exist.
- [ ] P0-1: all 28 B3 residual visible failures have a unique primary root cause.
- [ ] P0-1: execution, state, and egress authority-expansion counts are exact and trace-verifiable.
- [ ] P0-2: ICA and ASR have cluster-adjusted CIs for every evaluated configuration.
- [ ] P0-2: ASR includes small-cluster sensitivity analysis.
- [ ] P0-2: B3 pairwise effect sizes include Holm-corrected p-values.
- [ ] P0-3: parser fuzz family counts, seeds, coverage, latency, and oracle outputs are rebuildable.
- [ ] P0-4: each broker concurrency level has at least five independent runs.
- [ ] P0-4: broker reporting includes tail latency, resource use, drops, fail-open count, and authority-expansion count.
- [ ] P0-5: backend error, timeout, and rollback counts use consistent denominators.
- [ ] P0-5: backend comparisons use paired prompt-level analysis.
- [ ] P0-6: timing IID-vs-HMM paired delta AUC is rebuildable.
- [ ] P0-6: cross-path timing is evaluated or explicitly retained as a limitation.
- [ ] P0-7: human audit reports three pairwise kappas and one multi-rater agreement statistic.
- [ ] P0-8: all main tables and CIs are generated from the same artifact commit.

## P1 Completion Checklist

- [ ] P1-1: GreyNoise threshold sensitivity for unique-command thresholds 3, 5, and 10 is rebuildable.
- [ ] P1-1: field results remain labeled as observational evidence.
- [ ] P1-2: B3-ERRSIM and B3-HardRefusal are paired except for response policy.
- [ ] P1-2: detection criteria are preregistered before analysis.
- [ ] P1-2: ERRSIM claims are reduced if no direct baseline supports them.

## Output Files Required for Release Artifact

The release artifact should contain at least the following files:

| File | Purpose |
|---|---|
| `baseline_ablation_results.csv` | Canonical ablation summary for ICA/ASR baselines and B3. |
| `prompt_injection_expanded_results.csv` | Canonical prompt-injection and residual-failure probe results. |
| `model_generalization_results.csv` | Canonical four-backend/model generalization results. |
| `containment_stress_results.csv` | Canonical containment stress-test outcomes. |
| `svl_state_poisoning_results.csv` | Canonical SVL state-poisoning outcomes. |
| `benign_false_positive_results.csv` | Canonical benign-command false-positive outcomes. |
| `timing_sequence_results.csv` | Canonical timing sequence and paired delta-AUC outcomes. |
| `broker_load_results.csv` | Canonical broker load repeated-run outcomes. |
| `parser_fuzz_results.csv` | Canonical parser fuzz case/campaign outcomes. |
| `errsim_ablation_results.csv` | Canonical ERRSIM-vs-hard-refusal ablation outcomes. |
| `authority_path_decomposition.csv` | P0-1 authority-path decomposition for residual failures. |
| `human_audit_labels.csv` | P0-7 de-identified reviewer labels. |
| `field_filtering_sensitivity.csv` | P1-1 threshold and GreyNoise sensitivity. |
| `artifact_manifest.json` | Checksums, provenance, and release status. |
| `DATA_DICTIONARY.md` | Column definitions and semantics. |
| `REPRODUCIBILITY.md` | Rebuild environment and command documentation. |

## Rebuild Targets

The artifact should expose these commands as the stable public interface:

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

## Recommended Execution Order

1. Decompose the 28 residual B3 failures by authority path.
2. Recompute cluster-adjusted ICA/ASR CIs and effect sizes.
3. Add parser fuzz campaign metadata and coverage.
4. Repeat broker load runs at each concurrency level.
5. Normalize four-backend denominators, rates, and paired comparisons.
6. Recompute timing paired delta AUC.
7. Run the cross-path timing experiment.
8. Add full human-audit agreement statistics.
9. Complete the artifact manifest and one-command rebuild path.
10. Run GreyNoise threshold sensitivity.
11. Run the ERRSIM-vs-hard-refusal direct ablation.
