# Limitations and unavailable claims

This repository intentionally excludes source code whose redistribution rights are unresolved, third-party weights and datasets, publication PDFs, raw private experiment records, and qualitative image assets. As a result, the released empirical summaries are traceable but not publicly replayable.

Blocked claims include patch-L2 seed discrimination, private-model forgery, embedding training, the n/b ablation, steganalysis removal, latent forgery, object-scale CAT behavior, insertion semantics, regeneration removal, COCO generation quality, and direct no-proxy alternatives. They remain `BLOCKED / NONE`, not failed experiments.

Several analytical properties are documented as diagnostic rather than empirical reproduction outcomes. Qualitative figures without objective evaluation laws are non-evaluable. Full details are in `provenance/claim_outcomes.csv`.

Observed zero false positives in finite samples do not establish a population false-positive rate of zero. Bootstrap intervals describe the reproduced sample and are not tests of equality with paper targets. The project does not establish robustness against all attacks or generalization to other models and datasets.

