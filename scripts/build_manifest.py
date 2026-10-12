#!/usr/bin/env python3
"""Build the non-circular SHA-256 manifest for curated scientific artifacts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVISION = "498d4b25446003260d9367c10b1fdb27eb9988a1"

SPECS = {
    "results/clean_detector/summary.csv": ("RESULT_SUMMARY", "SUPPORTING_CLEAN_DETECTOR", "repro/CALIBRATION_10_REPORT.md; repro/HELDOUT_20_REPORT.md; repro/CONFIRMATORY_30_REPORT.md; repro/CLEAN_DETECTOR_50_SUMMARY.md", "888bd856b5085723df2b5a75d511319d0d03259e;e64839be99f7df30bfa5de43982d1165a9b49736;aab444589446314ef0b4bbee58b870c76691dea0;c5c1a0e9f8783809fdbb8f862b802d4a9ad125b0", "B", "SUMMARY_ONLY", "Calibration is not independent; record-level outputs remain private."),
    "results/transformation_robustness/summary.csv": ("RESULT_SUMMARY", "TRANSFORM_ROBUSTNESS", "repro/TRANSFORM_ROBUSTNESS_30_REPORT.md", "7e1e7b7cc6f0c3a63855e960f6b461ea31e6bb13", "B", "SUMMARY_ONLY", "No authorized numeric tolerance; outcome is INCONCLUSIVE."),
    "results/cat_attack/summary.csv": ("RESULT_SUMMARY", "CAT_ATTACK_BASIC_AUC; CAT_ATTACK_SPATIAL_AUC; CAT_ATTACK_LOCALIZATION_SIGNAL", "repro/CAT_ATTACK_30_REPORT.md", "6abe800ad310fe4c0500accf1aca13d49d6b4908", "B", "SUMMARY_ONLY", "Surrogate cat asset; exact publication asset and some protocol details unavailable."),
    "results/caption_embedding/summary.csv": ("RESULT_SUMMARY", "EMBEDDING_ABLATION", "repro/CAPTION_EMBEDDING_ABLATION_SUMMARY.json", "c896f36f7c94ffd97902200bcbe985fa3545ab3b", "B", "SUMMARY_ONLY", "Released fine-tuned artifact evaluated; training process not reproduced."),
    "results/generation_quality/summary.json": ("RESULT_SUMMARY", "GEN_QUALITY_SD_PROMPTS", "repro/GENERATION_QUALITY_ANALYSIS.json", "6a95fe1a6c412a642ac89492d548cac31571166c", "B", "SUMMARY_ONLY", "Private paired records; metric is source-defined, not standardized CLIPScore."),
    "results/semantic_angle/coverage.json": ("RESULT_SUMMARY", "SEMANTIC_ANGLE_EMPIRICAL_CURVE", "repro/level-max/CANONICAL_STATE_SNAPSHOT_d855949898275847de290806da075d0fe7efe3f9f4ad320553a2891338f079cf.json", "1f2f7566e942f8b0e325824d10181f4f4c785fd5", "B", "SUMMARY_ONLY", "Private selected records; publication mapping and comparison rule unresolved."),
    "figures/clean_detector.svg": ("VECTOR_FIGURE", "SUPPORTING_CLEAN_DETECTOR", "results/clean_detector/summary.csv", "DERIVED_FROM_RELEASED_SUMMARY", "B", "SUMMARY_ONLY", "No uncertainty interval shown; calibration is not independent."),
    "figures/transformation_robustness.svg": ("VECTOR_FIGURE", "TRANSFORM_ROBUSTNESS", "results/transformation_robustness/summary.csv", "DERIVED_FROM_RELEASED_SUMMARY", "B", "SUMMARY_ONLY", "No confidence intervals invented; outcome remains INCONCLUSIVE."),
    "figures/caption_embedding.svg": ("VECTOR_FIGURE", "EMBEDDING_ABLATION", "results/caption_embedding/summary.csv", "DERIVED_FROM_RELEASED_SUMMARY", "B", "SUMMARY_ONLY", "Full-scale means shown; does not reproduce embedding training."),
    "provenance/claim_outcomes.csv": ("CLAIM_MAP", "ALL_31_CLAIMS", "repro/level-max/CANONICAL_STATE_SNAPSHOT_d855949898275847de290806da075d0fe7efe3f9f4ad320553a2891338f079cf.json", "1f2f7566e942f8b0e325824d10181f4f4c785fd5", "MIXED_B_C", "SUMMARY_ONLY", "Preserves final canonical axes; not a substitute for unavailable protocols."),
    "provenance/reproducibility_levels.csv": ("REPRODUCIBILITY_MAP", "RELEASED_RESULTS", "curation assessment", "INDEPENDENTLY_AUTHORED", "MIXED_B_C", "SUMMARY_ONLY", "Levels describe this package, not the private archive."),
    "provenance/source_versions.json": ("SOURCE_BINDING", "RELEASED_RESULTS", "frozen private authority", "INDEPENDENTLY_AUTHORED", "MIXED_B_C", "METADATA_ONLY", "Private archive identifiers are not public download links."),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    artifacts = []
    for public_path, spec in sorted(SPECS.items()):
        path = ROOT / public_path
        if not path.is_file():
            raise SystemExit(f"missing artifact: {public_path}")
        artifact_type, claim, source_path, source_hash, level, availability, limitation = spec
        artifacts.append({
            "PUBLIC_PATH": public_path,
            "ARTIFACT_TYPE": artifact_type,
            "SCIENTIFIC_CLAIM": claim,
            "SOURCE_REVISION": REVISION,
            "SOURCE_PATH": source_path,
            "SOURCE_GIT_BLOB_OR_SHA256": source_hash,
            "RELEASED_SHA256": sha256(path),
            "PUBLIC_REPRODUCIBILITY_LEVEL": level,
            "INPUT_AVAILABILITY": availability,
            "LICENSE_STATUS": "NO_LICENSE_GRANTED_PENDING_CONTRIBUTOR_APPROVAL",
            "LIMITATIONS": limitation,
        })
    payload = {"schema_version": "1.0", "artifact_count": len(artifacts), "artifacts": artifacts}
    target = ROOT / "provenance" / "artifact_manifest.json"
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {target.relative_to(ROOT)} with {len(artifacts)} artifacts")


if __name__ == "__main__":
    main()

