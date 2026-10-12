# Licensing and redistribution inventory

## Current status

No repository-wide license is granted. The repository remains a private release candidate. Public availability of the upstream SEAL implementation was not interpreted as permission to redistribute it, and no license is granted on behalf of an unverified rights holder.

## Independently authored Python code

| File | Authorship basis | Upstream derivation | Third-party bytes | Redistributability status | Proposed license | Approval still required |
|---|---|---|---|---|---|---|
| `scripts/build_manifest.py` | Created for this independent reproduction package; Git history identifies the contributor but does not by itself prove exclusive rights | No upstream SEAL code copied | Python standard library interfaces only | Candidate original code; approval pending | MIT or Apache-2.0 | Contributor/rightsholder must explicitly select and grant the code license |
| `scripts/verify_release.py` | Created for this independent reproduction package; Git history identifies the contributor but does not by itself prove exclusive rights | No upstream SEAL code copied | Python standard library interfaces only | Candidate original code; approval pending | MIT or Apache-2.0 | Contributor/rightsholder must explicitly select and grant the code license |
| `scripts/test_negative_mutations.py` | Created for this independent reproduction package; Git history identifies the contributor but does not by itself prove exclusive rights | No upstream SEAL code copied | Python standard library interfaces only | Candidate original code; approval pending | MIT or Apache-2.0 | Contributor/rightsholder must explicitly select and grant the code license |

## Other included categories

| Category | Included material | Authorship/derivation assessment | Third-party material | Proposed treatment | Remaining approval |
|---|---|---|---|---|---|
| Documentation | `README.md`, `REPRODUCE.md`, `docs/`, `figures/README.md` | Independently written academic curation; factual references to SEAL do not convey ownership of SEAL | Links, names, and citations only; no publication PDF or upstream prose intentionally copied | CC BY 4.0 | Confirm contributor/rightsholder authority and explicitly grant CC BY 4.0 |
| Aggregate scientific summaries | `results/` | Factual values normalized from the frozen private reproduction authority | No raw records, model weights, datasets, or image assets | Separate explicit data-license decision | Determine database/data rights and approve a specific data license or public-domain dedication where legally valid |
| SVG figures | `figures/*.svg` | Independently authored static editorial charts of aggregate values | No third-party image bytes | CC BY 4.0 if contributor authority is confirmed | Explicit contributor/rightsholder approval |
| Claim and provenance metadata | `provenance/*.csv`, `provenance/*.json` | Independently structured factual metadata derived from frozen authority | Private archive identifiers only; no private archive bytes | Separate data/metadata license determination | Confirm rights and select explicit terms |

## Excluded material

- Original or adapted SEAL implementation code: excluded because the verified upstream snapshot has no explicit root license.
- Model weights, datasets, publication PDFs, private raw records, cloud/runtime records, and external images: excluded.
- CAT index-94 qualitative imagery: excluded because redistribution rights for the source image and pasted attack asset were not established.
- MultiSEAL manuscript and results: excluded; this package makes no independent MultiSEAL claim.

## Concrete recommendation and unresolved approvals

1. Select either MIT or Apache-2.0 for the three independently authored Python scripts, after all relevant contributors/rightsholders explicitly approve.
2. Use CC BY 4.0 for independently authored documentation and SVG editorial charts, after explicit contributor/rightsholder approval.
3. Make a separate, explicit determination for scientific summary data and structured claim/provenance metadata; do not assume the code or documentation license covers them.
4. Only after those approvals are recorded should corresponding license files or per-file notices be added and public visibility be considered.

Until then, status remains `NO_LICENSE_GRANTED_PENDING_CONTRIBUTOR_APPROVAL`.
