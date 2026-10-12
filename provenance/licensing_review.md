# Licensing and redistribution review

## Candidate status

No repository-wide license is granted. Public GitHub availability of the upstream implementation was not treated as permission to redistribute it. This private candidate is designed for later rights review before any visibility change.

## Included categories

- **A — independently authored reproduction code:** `scripts/verify_release.py` and `scripts/build_manifest.py`.
- **E — scientific data/artifact:** normalized summaries under `results/`, claim and reproducibility maps under `provenance/`, and SVG charts under `figures/`. These are derived factual summaries; contributor authority to apply an explicit data license still requires confirmation.
- **F — documentation:** `README.md`, `REPRODUCE.md`, `docs/`, and provenance documentation.

## Excluded categories

- **B/C — derived or copied upstream code:** all original SEAL scripts excluded because the verified upstream snapshot has no explicit root license.
- **D — third-party dependencies/assets:** model weights, datasets, paper/supplement PDFs, and external images excluded.
- CAT index-94 qualitative figure excluded because redistribution rights for the source image and pasted attack asset were not established.
- Private raw records and cloud/runtime material excluded from this academic candidate.

## Recommendation

After confirming contributor ownership and approval, the maintainers could license the independently authored Python scripts under MIT or Apache-2.0 and documentation under CC BY 4.0. Scientific summary data should receive a separately explicit data-license decision. Those recommendations are not grants; do not add a `LICENSE` file or make the repository public until approvals are recorded.

