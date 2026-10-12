# Licensing and file-level provenance review

## Owner declaration and authorization

On 2026-10-12, the repository owner declared that the project was conducted
and directed by the owner with AI assistance from CO1/CO2 and that no other
human research contributor participated in creating the independent package.
The owner authorized MIT for the three original scripts and CC BY 4.0 for
original documentation, SVG figures, aggregate compilations and structured
metadata to the extent the owner holds the rights. This review relies on that
declaration; it is not a claim that every AI-generated element is copyrightable.

Licensor/attribution: Tien Dung (`tiendungeaknop-deptrai`). Exact grants and
path coverage are in `LICENSE_SCOPE.md`. There is no blanket claim of ownership
of all referenced research or third-party material.

## Audited file inventory

| Paths | Provenance class | Derivation and third-party assessment | Applied license |
|---|---|---|---|
| `scripts/build_manifest.py` | Original AI-assisted project code | Package integrity tooling authored for the independent package; no SEAL implementation copied; standard-library APIs only | MIT |
| `scripts/verify_release.py` | Original AI-assisted project code with factual constants | Original validator; reviewed expectations are factual summaries; no upstream scientific implementation copied | MIT |
| `scripts/test_negative_mutations.py` | Original AI-assisted project code | Original isolated fixture and mutation testing; no upstream code copied | MIT |
| `README.md`, `REPRODUCE.md`, `LICENSE_SCOPE.md`, `docs/*.md`, `figures/README.md`, `provenance/licensing_review.md` | Original AI-assisted project documentation | Independent explanatory text; SEAL authors remain credited; source citations do not convey ownership of SEAL | CC BY 4.0, owner-held rights only |
| `figures/caption_embedding.svg`, `figures/clean_detector.svg`, `figures/transformation_robustness.svg` | Original AI-assisted editorial charts | Static vector renderings of released aggregate values; no third-party image bytes or invented scientific samples | CC BY 4.0, owner-held rights only |
| `results/caption_embedding/summary.csv`, `results/cat_attack/summary.csv`, `results/clean_detector/summary.csv`, `results/transformation_robustness/summary.csv`, `results/generation_quality/summary.json`, `results/semantic_angle/coverage.json` | Factual scientific summary compilations | Normalized facts from bound private reproduction artifacts; paper targets are identified as references; no claim of exclusive rights in individual facts | CC BY 4.0 for original compilation/arrangement and any owner-held database rights |
| `provenance/claim_outcomes.csv`, `provenance/reproducibility_levels.csv`, `provenance/source_versions.json`, `provenance/artifact_manifest.json` | Original structured factual metadata | Original structure and curation; exact external source identifiers do not license external bytes | CC BY 4.0, owner-held rights only |
| `.gitignore`, `.gitattributes` | Original project configuration | No upstream adaptation identified | CC BY 4.0 to the extent protectable |
| `LICENSES/MIT.txt` | Standard MIT license instrument with project notice | Standard terms, not original project code | Standard license instrument |
| `LICENSES/CC-BY-4.0.txt` | Official Creative Commons license instrument | Retrieved unchanged from the official URL; the instrument dedicates its license text to the public domain under CC0 | Standard license instrument; CC0 text dedication |

The manifest records license status and license-file locator for every hashed
file. The manifest itself is covered by the explicit scope notice and excluded
only from its own hash to avoid a cycle.

## License-text provenance

The complete CC BY 4.0 legal text was retrieved on 2026-10-12 from
https://creativecommons.org/licenses/by/4.0/legalcode.txt.
SHA-256 of the retrieved bytes:
`9ba9550ad48438d0836ddab3da480b3b69ffa0aac7b7878b5a0039e7ab429411`.
The local license text includes its full attribution requirements, disclaimers
and other terms. The owner authorization applies the license; it does not amend
the legal text.

## Exclusions and remaining rights

No unresolved upstream derivation was identified in the proposed licensed
project files. No further human contributor approval is pending under the
owner's declaration. Copyrightability of AI-assisted elements is not asserted;
the grant extends only to rights actually held by the owner.

Upstream SEAL code, publication PDFs, third-party models, datasets, external
images, raw private records and CAT index-94 imagery remain excluded. Their
rights are not resolved or granted by this action. Factual references to those
sources and to SEAL do not imply author endorsement. MultiSEAL material is
excluded.

Current licensing authority is this review, `LICENSE_SCOPE.md` and the owner's
declaration. Public visibility and paper link insertion remain on hold.
