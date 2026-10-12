# Independent Reproduction of SEAL

This private release candidate documents an independent reproduction of **SEAL: Semantic Aware Image Watermarking** by Kasra Arabi, R. Teal Witter, Chinmay Hegde, and Niv Cohen (ICCV 2025). The reproduction maintainers do **not** claim to have invented SEAL. Public release is neither complete nor authorized.

- Original paper: <https://openaccess.thecvf.com/content/ICCV2025/html/Arabi_SEAL_Semantic_Aware_Image_Watermarking_ICCV_2025_paper.html>
- Original implementation: <https://github.com/Kasraarabi/SEAL>, pinned for this study at `92d31b31b93a6e373fe88a584c640beafb68c6fa`
- This repository: independently authored documentation, normalized result summaries, vector charts, and integrity tooling for the reproduction.

This repository is not a fork and contains no copied SEAL source code, model weights, datasets, publication PDFs, or third-party image assets. It also contains no MultiSEAL manuscript or independent MultiSEAL result.

## Scope and headline findings

The package records the final state of 31 scientific claims plus one supporting clean-detector result. Seven claims were empirically evaluated: caption/embedding was **REPRODUCED**; transformation robustness, three CAT-attack claims, Stable-Diffusion-Prompts generation quality, and the semantic-angle curve were **INCONCLUSIVE** under the frozen decision rules. Other claims are analytical, non-evaluable, or blocked because required public protocols/assets are unavailable. `BLOCKED` means not executable from current public authority; it does not mean experimentally disproved.

The clean detector was also evaluated as a supporting result. Frozen held-out and confirmatory stages each achieved image-level ROC-AUC 0.90, with no observed false positives in their respective controls. Calibration AUC 1.00 is not an independent test.

| Result | Scale | Released finding | Level |
|---|---:|---|:---:|
| Clean detector | calibration 10/10; held-out 20/20; confirmatory 30/30 | AUC 1.00 calibration; 0.90 held-out; 0.90 confirmatory | B |
| Transformation robustness | 30 positives + 30 controls per condition | seven AUCs; outcome INCONCLUSIVE | B |
| CAT attack | 30 paired source images | basic/spatial AUC and localization summaries; outcome INCONCLUSIVE | B |
| Caption/embedding | 1,000 per configuration; 3,000 total | `none_clip < blip2_original < blip2_finetuned`; REPRODUCED | B |
| Generation quality | 100 paired observations | mean paired delta +0.7461, 95% CI [0.1876, 1.3111]; INCONCLUSIVE | B |
| Semantic angle | 549 selected records | 27/30 bins populated; INCONCLUSIVE | B |

## Reproducibility levels

- **Level A — publicly replayable:** distributed record-level data and analysis are sufficient to recompute the result. This candidate contains no Level A scientific result.
- **Level B — traceable, not publicly replayable:** checked summaries, exact source bindings, methods, and hashes are present, but record-level inputs remain private or cannot be redistributed.
- **Level C — not independently executable or evaluable:** current public source or protocol is insufficient.

The verification command validates released bytes and frozen metadata; it does not rerun Stable Diffusion, SEAL, or the original experiments:

```bash
python scripts/verify_release.py
```

See [REPRODUCE.md](REPRODUCE.md), [methodology](docs/methodology.md), [protocols](docs/experimental_protocols.md), [deviations](docs/deviations.md), and [limitations](docs/limitations.md).

## Figures and data

All included figures are independently authored SVG charts rendered from the released summary tables. No qualitative CAT image is included because redistribution rights for the constituent image and attack asset were not established. Figure provenance is recorded in `figures/README.md` and the artifact manifest.

## Citation and licensing status

Please cite the original SEAL paper for the method. No `CITATION.cff` is supplied. The project owner, Tien Dung (`tiendungeaknop-deptrai`), conducted and directed this package with AI assistance, according to the owner's declaration.

| Material | License |
|---|---|
| Three original Python scripts in `scripts/` | [MIT](LICENSES/MIT.txt) |
| Original documentation, SVG figures, aggregate result compilations and structured metadata | [CC BY 4.0](LICENSES/CC-BY-4.0.txt), only to the extent rights are held by the project owner |

See [LICENSE_SCOPE.md](LICENSE_SCOPE.md) for exact path coverage, attribution and exclusions, and [licensing review](provenance/licensing_review.md) for the provenance audit. Individual scientific facts are not claimed as exclusive property. These licenses do not cover upstream SEAL or third-party assets. Public visibility and paper link insertion remain on hold.

## Limitations

Summary-level release supports inspection and integrity checking, not full replay. Several source assets and protocols remain unavailable; surrogate CAT imagery was used in the private scientific run; and absence of a pre-result numeric tolerance leaves multiple measurements inconclusive. Do not interpret proximity to paper values as reproduction success.

