#!/usr/bin/env python3
"""Build a deterministic, non-circular manifest for every tracked release file."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = "provenance/artifact_manifest.json"
AUTHORITY_REVISION = "498d4b25446003260d9367c10b1fdb27eb9988a1"
LICENSE_STATUS = "NO_LICENSE_GRANTED_PENDING_CONTRIBUTOR_APPROVAL"


def authority(path: str, blob: str) -> dict[str, str]:
    return {"SOURCE_REVISION": AUTHORITY_REVISION, "SOURCE_PATH": path, "SOURCE_GIT_BLOB_OR_SHA256": blob}


SCIENTIFIC_METADATA: dict[str, dict[str, object]] = {
    "results/clean_detector/summary.csv": {
        "ARTIFACT_TYPE": "RESULT_SUMMARY", "SCIENTIFIC_CLAIM": "SUPPORTING_CLEAN_DETECTOR",
        "SOURCES": [
            authority("repro/DETECTOR_CALIBRATION_10_REPORT.md", "24ee28292d766f3ce7c8f50fc132ef6298f9e204"),
            authority("repro/HELDOUT_20_REPORT.md", "e64839be99f7df30bfa5de43982d1165a9b49736"),
            authority("repro/CONFIRMATORY_30_REPORT.md", "aab444589446314ef0b4bbee58b870c76691dea0"),
            authority("repro/CLEAN_DETECTOR_50_SUMMARY.md", "c5c1a0e9f8783809fdbb8f862b802d4a9ad125b0"),
        ], "PUBLIC_REPRODUCIBILITY_LEVEL": "B", "INPUT_AVAILABILITY": "SUMMARY_ONLY",
        "LIMITATIONS": "Calibration is not independent; record-level outputs remain private.",
    },
    "results/transformation_robustness/summary.csv": {
        "ARTIFACT_TYPE": "RESULT_SUMMARY", "SCIENTIFIC_CLAIM": "TRANSFORM_ROBUSTNESS",
        "SOURCES": [authority("repro/TRANSFORM_ROBUSTNESS_30_REPORT.md", "7e1e7b7cc6f0c3a63855e960f6b461ea31e6bb13")],
        "PUBLIC_REPRODUCIBILITY_LEVEL": "B", "INPUT_AVAILABILITY": "SUMMARY_ONLY",
        "LIMITATIONS": "No authorized numeric tolerance; outcome is INCONCLUSIVE.",
    },
    "results/cat_attack/summary.csv": {
        "ARTIFACT_TYPE": "RESULT_SUMMARY", "SCIENTIFIC_CLAIM": "CAT_ATTACK_BASIC_AUC; CAT_ATTACK_SPATIAL_AUC; CAT_ATTACK_LOCALIZATION_SIGNAL",
        "SOURCES": [authority("repro/CAT_ATTACK_30_REPORT.md", "6abe800ad310fe4c0500accf1aca13d49d6b4908")],
        "PUBLIC_REPRODUCIBILITY_LEVEL": "B", "INPUT_AVAILABILITY": "SUMMARY_ONLY",
        "LIMITATIONS": "Surrogate cat asset; exact publication asset and some protocol details unavailable.",
    },
    "results/caption_embedding/summary.csv": {
        "ARTIFACT_TYPE": "RESULT_SUMMARY", "SCIENTIFIC_CLAIM": "EMBEDDING_ABLATION",
        "SOURCES": [authority("repro/level-max/campaign-c/CAMPAIGN_C_FINAL_CLOSURE.json", "bdd95c871cf2294fa300c75cade1b62c3529c2a5")],
        "PUBLIC_REPRODUCIBILITY_LEVEL": "B", "INPUT_AVAILABILITY": "SUMMARY_ONLY",
        "LIMITATIONS": "Released fine-tuned artifact evaluated; training process not reproduced.",
    },
    "results/generation_quality/summary.json": {
        "ARTIFACT_TYPE": "RESULT_SUMMARY", "SCIENTIFIC_CLAIM": "GEN_QUALITY_SD_PROMPTS",
        "SOURCES": [authority("repro/GENERATION_QUALITY_ANALYSIS.json", "6a95fe1a6c412a642ac89492d548cac31571166c")],
        "PUBLIC_REPRODUCIBILITY_LEVEL": "B", "INPUT_AVAILABILITY": "SUMMARY_ONLY",
        "LIMITATIONS": "Private paired records; metric is source-defined, not standardized CLIPScore.",
    },
    "results/semantic_angle/coverage.json": {
        "ARTIFACT_TYPE": "RESULT_SUMMARY", "SCIENTIFIC_CLAIM": "SEMANTIC_ANGLE_EMPIRICAL_CURVE",
        "SOURCES": [authority("repro/level-max/campaign-a/CAMPAIGN_A_RESULT.json", "d3cf248a2279e238ac660ff0d2c3a62db95e5872")],
        "PUBLIC_REPRODUCIBILITY_LEVEL": "B", "INPUT_AVAILABILITY": "SUMMARY_ONLY",
        "LIMITATIONS": "Private selected records; publication mapping and comparison rule unresolved.",
    },
    "provenance/claim_outcomes.csv": {
        "ARTIFACT_TYPE": "CLAIM_MAP", "SCIENTIFIC_CLAIM": "ALL_31_CLAIMS",
        "SOURCES": [authority("repro/level-max/CANONICAL_STATE_SNAPSHOT_d855949898275847de290806da075d0fe7efe3f9f4ad320553a2891338f079cf.json", "1f2f7566e942f8b0e325824d10181f4f4c785fd5")],
        "PUBLIC_REPRODUCIBILITY_LEVEL": "MIXED_B_C", "INPUT_AVAILABILITY": "SUMMARY_ONLY",
        "LIMITATIONS": "Preserves final canonical axes; not a substitute for unavailable protocols.",
    },
    "provenance/source_versions.json": {
        "ARTIFACT_TYPE": "SOURCE_BINDING", "SCIENTIFIC_CLAIM": "RELEASED_RESULTS",
        "SOURCES": [authority("repro/MODEL_MANIFEST.md", "2dfdbc4a9ab40c0b7715d253ee1c1f5deb39f0b9"), authority("repro/REMAINING_CLAIMS_MODEL_MANIFEST.md", "4acd3b75d5b625f80017597233d89abda4ce6be3")],
        "PUBLIC_REPRODUCIBILITY_LEVEL": "MIXED_B_C", "INPUT_AVAILABILITY": "METADATA_ONLY",
        "LIMITATIONS": "Private archive identifiers are provenance locators, not public download links.",
    },
}

FIGURE_SOURCES = {
    "figures/clean_detector.svg": ("SUPPORTING_CLEAN_DETECTOR", "results/clean_detector/summary.csv", "No uncertainty interval shown; calibration is not independent."),
    "figures/transformation_robustness.svg": ("TRANSFORM_ROBUSTNESS", "results/transformation_robustness/summary.csv", "No confidence intervals invented; outcome remains INCONCLUSIVE."),
    "figures/caption_embedding.svg": ("EMBEDDING_ABLATION", "results/caption_embedding/summary.csv", "Full-scale means shown; byte-exact renderer is not supplied."),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tracked_paths() -> list[str]:
    result = subprocess.run(["git", "-C", str(ROOT), "ls-files"], check=True, capture_output=True, text=True)
    return sorted(line.replace("\\", "/") for line in result.stdout.splitlines() if line)


def metadata_for(public_path: str) -> dict[str, object]:
    if public_path in SCIENTIFIC_METADATA:
        return dict(SCIENTIFIC_METADATA[public_path])
    if public_path in FIGURE_SOURCES:
        claim, source_path, limitation = FIGURE_SOURCES[public_path]
        return {
            "ARTIFACT_TYPE": "VECTOR_FIGURE", "SCIENTIFIC_CLAIM": claim,
            "SOURCES": [{"SOURCE_REVISION": "THIS_RELEASE", "SOURCE_PATH": source_path, "SOURCE_GIT_BLOB_OR_SHA256": sha256(ROOT / source_path)}],
            "PUBLIC_REPRODUCIBILITY_LEVEL": "B", "INPUT_AVAILABILITY": "SUMMARY_ONLY", "LIMITATIONS": limitation,
        }
    return {
        "ARTIFACT_TYPE": "CODE" if Path(public_path).suffix.lower() == ".py" else "DOCUMENTATION_OR_METADATA",
        "SCIENTIFIC_CLAIM": "PACKAGE_SUPPORT", "SOURCES": [],
        "PUBLIC_REPRODUCIBILITY_LEVEL": "NOT_A_SCIENTIFIC_RESULT", "INPUT_AVAILABILITY": "NOT_APPLICABLE",
        "LIMITATIONS": "Independently authored package support file.",
    }


def main() -> None:
    tracked = tracked_paths()
    if MANIFEST_PATH not in tracked:
        raise SystemExit(f"tracked manifest missing: {MANIFEST_PATH}")
    covered = [path for path in tracked if path != MANIFEST_PATH]
    files = []
    for public_path in covered:
        path = ROOT / public_path
        if not path.is_file():
            raise SystemExit(f"tracked file missing: {public_path}")
        record = {"PUBLIC_PATH": public_path, **metadata_for(public_path)}
        record["RELEASED_SHA256"] = sha256(path)
        record["LICENSE_STATUS"] = LICENSE_STATUS
        files.append(record)
    payload = {
        "schema_version": "2.0", "hash_algorithm": "SHA-256", "non_circular_exclusions": [MANIFEST_PATH],
        "tracked_file_count_including_manifest": len(tracked), "manifested_file_count": len(files),
        "no_unmanifested_tracked_files": True, "files": files,
    }
    target = ROOT / MANIFEST_PATH
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {MANIFEST_PATH} with {len(files)}/{len(tracked)} non-circular file hashes")


if __name__ == "__main__":
    main()
