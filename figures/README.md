# Figure provenance

All figures are independently authored vector charts generated from released summary tables in this repository. They contain no third-party image bytes.

| Figure | Purpose | Source | N | Limitation |
|---|---|---|---:|---|
| `clean_detector.svg` | Separate calibration from frozen evaluation | `results/clean_detector/summary.csv` | 10/10, 20/20, 30/30 | calibration is not independent; pooled summary omitted |
| `transformation_robustness.svg` | Compare seven condition-level AUCs | `results/transformation_robustness/summary.csv` | 30 positives + 30 controls/condition | outcome remains inconclusive; no CI invented |
| `caption_embedding.svg` | Show the full-scale qualitative ordering | `results/caption_embedding/summary.csv` | 1,000/configuration | evaluates released artifact, not training |

The CAT index-94 qualitative figure was deliberately excluded because redistribution rights for the constituent image and attack asset were unresolved. Generation-quality and semantic-angle values remain available as machine-readable summaries; no additional figure was needed for clear communication.

