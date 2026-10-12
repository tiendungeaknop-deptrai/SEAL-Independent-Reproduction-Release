#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tien Dung (tiendungeaknop-deptrai)
"""Verify full package integrity, canonical axes, authorities, and released values."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

MANIFEST_PATH = "provenance/artifact_manifest.json"
AXES = ("resolution_state", "outcome", "fidelity", "scale_basis", "finality")
EXPECTED_ROWS = """THEORY_DETECTION_PROBABILITY_LEMMA|DIAGNOSTIC_ONLY|NONE|EXACT_PUBLIC_PROTOCOL|UNKNOWN_N|FINAL
PATCH_L2_SEED_DISCRIMINATION|BLOCKED|NONE|UNRESOLVED|UNKNOWN_N|FINAL
SEMANTIC_ANGLE_EMPIRICAL_CURVE|EVALUATED|INCONCLUSIVE|SOURCE_FAITHFUL_WITH_DEVIATION|SOURCE_DEFAULT_N|FINAL
EMBEDDING_ABLATION|EVALUATED|REPRODUCED|SOURCE_FAITHFUL_WITH_DEVIATION|SOURCE_DEFAULT_N|FINAL
CAT_ATTACK|NON_EVALUABLE|NONE|UNRESOLVED|UNKNOWN_N|FINAL
CAT_ATTACK_BASIC_AUC|EVALUATED|INCONCLUSIVE|SOURCE_FAITHFUL_WITH_DEVIATION|REDUCED_N|FINAL
CAT_ATTACK_SPATIAL_AUC|EVALUATED|INCONCLUSIVE|SOURCE_FAITHFUL_WITH_DEVIATION|REDUCED_N|FINAL
CAT_ATTACK_LOCALIZATION_SIGNAL|EVALUATED|INCONCLUSIVE|SOURCE_FAITHFUL_WITH_DEVIATION|REDUCED_N|FINAL
TRANSFORM_ROBUSTNESS|EVALUATED|INCONCLUSIVE|SOURCE_FAITHFUL_WITH_DEVIATION|REDUCED_N|FINAL
PRIVATE_MODEL_FORGERY_AUC|BLOCKED|NONE|UNRESOLVED|UNKNOWN_N|FINAL
EMBEDDING_TRAINING_PROCESS|BLOCKED|NONE|UNRESOLVED|UNKNOWN_N|FINAL
N_B_ABLATION|BLOCKED|NONE|UNRESOLVED|UNKNOWN_N|FINAL
STEGANALYSIS_REMOVAL|BLOCKED|NONE|UNRESOLVED|UNKNOWN_N|FINAL
LATENT_FORGERY|BLOCKED|NONE|UNRESOLVED|PAPER_N|FINAL
CAT_OBJECT_SCALE|BLOCKED|NONE|UNRESOLVED|UNKNOWN_N|FINAL
INSERTION_SEMANTICS|BLOCKED|NONE|UNRESOLVED|UNKNOWN_N|FINAL
REGENERATION_REMOVAL|BLOCKED|NONE|UNRESOLVED|UNKNOWN_N|FINAL
PROXY_VISUAL_COMPARISON|NON_EVALUABLE|NONE|UNRESOLVED|UNKNOWN_N|FINAL
GEN_QUALITY|NON_EVALUABLE|NONE|UNRESOLVED|UNKNOWN_N|FINAL
GEN_QUALITY_SD_PROMPTS|EVALUATED|INCONCLUSIVE|SOURCE_FAITHFUL_WITH_DEVIATION|SOURCE_DEFAULT_N|FINAL
GEN_QUALITY_COCO|BLOCKED|NONE|UNRESOLVED|SOURCE_DEFAULT_N|FINAL
GEN_QUALITY_VISUAL|NON_EVALUABLE|NONE|UNRESOLVED|UNKNOWN_N|FINAL
REPETITIVE_PATCH_VISUAL|NON_EVALUABLE|NONE|UNRESOLVED|UNKNOWN_N|FINAL
DISTORTION_FREE_GENERATION_PROPERTY|DIAGNOSTIC_ONLY|NONE|EXACT_PUBLIC_PROTOCOL|UNKNOWN_N|FINAL
DATABASE_FREE_DETECTION_PROPERTY|DIAGNOSTIC_ONLY|NONE|EXACT_PUBLIC_PROTOCOL|UNKNOWN_N|FINAL
ALTERNATIVE_NO_PROXY_DIRECT_WATERMARKING_CAPABILITY|BLOCKED|NONE|UNRESOLVED|UNKNOWN_N|FINAL
ALTERNATIVE_NO_PROXY_DIRECT_WATERMARK_QUALITY|BLOCKED|NONE|UNRESOLVED|UNKNOWN_N|FINAL
CONDITIONAL_NO_FALSE_IDENTIFICATION_PROPERTY|DIAGNOSTIC_ONLY|NONE|EXACT_PUBLIC_PROTOCOL|UNKNOWN_N|FINAL
SPATIAL_RECOVERY_COMPLEXITY|DIAGNOSTIC_ONLY|NONE|EXACT_PUBLIC_PROTOCOL|UNKNOWN_N|FINAL
SET_LEVEL_NOISE_CORRELATION_LEAKAGE|DIAGNOSTIC_ONLY|NONE|EXACT_PUBLIC_PROTOCOL|UNKNOWN_N|FINAL
SET_LEVEL_SALT_VARIATION_MITIGATION_TRADEOFF|DIAGNOSTIC_ONLY|NONE|UNRESOLVED|UNKNOWN_N|FINAL"""
EXPECTED_CLAIMS = {}
for line in EXPECTED_ROWS.splitlines():
    claim_id, *axes = line.split("|")
    EXPECTED_CLAIMS[claim_id] = tuple(axes)

EXPECTED_SOURCES = {
    "results/clean_detector/summary.csv": [
        ("repro/DETECTOR_CALIBRATION_10_REPORT.md", "24ee28292d766f3ce7c8f50fc132ef6298f9e204"),
        ("repro/HELDOUT_20_REPORT.md", "e64839be99f7df30bfa5de43982d1165a9b49736"),
        ("repro/CONFIRMATORY_30_REPORT.md", "aab444589446314ef0b4bbee58b870c76691dea0"),
        ("repro/CLEAN_DETECTOR_50_SUMMARY.md", "c5c1a0e9f8783809fdbb8f862b802d4a9ad125b0"),
    ],
    "results/caption_embedding/summary.csv": [("repro/level-max/campaign-c/CAMPAIGN_C_FINAL_CLOSURE.json", "bdd95c871cf2294fa300c75cade1b62c3529c2a5")],
    "results/transformation_robustness/summary.csv": [("repro/TRANSFORM_ROBUSTNESS_30_REPORT.md", "7e1e7b7cc6f0c3a63855e960f6b461ea31e6bb13")],
    "results/cat_attack/summary.csv": [("repro/CAT_ATTACK_30_REPORT.md", "6abe800ad310fe4c0500accf1aca13d49d6b4908")],
    "results/generation_quality/summary.json": [("repro/GENERATION_QUALITY_ANALYSIS.json", "6a95fe1a6c412a642ac89492d548cac31571166c")],
    "results/semantic_angle/coverage.json": [("repro/level-max/campaign-a/CAMPAIGN_A_RESULT.json", "d3cf248a2279e238ac660ff0d2c3a62db95e5872")],
    "provenance/claim_outcomes.csv": [("repro/level-max/CANONICAL_STATE_SNAPSHOT_d855949898275847de290806da075d0fe7efe3f9f4ad320553a2891338f079cf.json", "1f2f7566e942f8b0e325824d10181f4f4c785fd5")],
    "provenance/source_versions.json": [
        ("repro/MODEL_MANIFEST.md", "2dfdbc4a9ab40c0b7715d253ee1c1f5deb39f0b9"),
        ("repro/REMAINING_CLAIMS_MODEL_MANIFEST.md", "4acd3b75d5b625f80017597233d89abda4ce6be3"),
    ],
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tracked_paths(root: Path) -> set[str]:
    result = subprocess.run(["git", "-C", str(root), "ls-files"], check=True, capture_output=True, text=True)
    return {line.replace("\\", "/") for line in result.stdout.splitlines() if line}


def load_csv(root: Path, relative: str) -> list[dict[str, str]]:
    with (root / relative).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def require_equal(errors: list[str], label: str, actual: object, expected: object) -> None:
    if actual != expected:
        errors.append(f"{label}: expected {expected!r}, found {actual!r}")


def verify_manifest(root: Path, errors: list[str]) -> int:
    manifest = json.loads((root / MANIFEST_PATH).read_text(encoding="utf-8"))
    files = manifest.get("files", [])
    paths = [item.get("PUBLIC_PATH") for item in files]
    tracked = tracked_paths(root)
    expected_paths = tracked - {MANIFEST_PATH}
    require_equal(errors, "manifest schema", manifest.get("schema_version"), "2.0")
    require_equal(errors, "manifest exclusions", manifest.get("non_circular_exclusions"), [MANIFEST_PATH])
    require_equal(errors, "tracked count", manifest.get("tracked_file_count_including_manifest"), len(tracked))
    require_equal(errors, "manifested count", manifest.get("manifested_file_count"), len(files))
    require_equal(errors, "manifest coverage flag", manifest.get("no_unmanifested_tracked_files"), True)
    require_equal(errors, "manifest path set", set(paths), expected_paths)
    if len(paths) != len(set(paths)):
        errors.append("duplicate manifest PUBLIC_PATH")
    for item in files:
        path = root / item["PUBLIC_PATH"]
        if not path.is_file():
            errors.append(f"missing tracked file: {item['PUBLIC_PATH']}")
        elif sha256(path) != item.get("RELEASED_SHA256"):
            errors.append(f"hash mismatch: {item['PUBLIC_PATH']}")
        if not isinstance(item.get("SOURCES"), list):
            errors.append(f"SOURCES is not an array: {item['PUBLIC_PATH']}")
        relative = item["PUBLIC_PATH"]
        if relative in {"scripts/build_manifest.py", "scripts/verify_release.py", "scripts/test_negative_mutations.py"}:
            expected_license, expected_file = "MIT", "LICENSES/MIT.txt"
        elif relative.startswith("LICENSES/"):
            expected_license, expected_file = "STANDARD_LICENSE_TEXT", relative
        else:
            expected_license, expected_file = "CC-BY-4.0", "LICENSES/CC-BY-4.0.txt"
        require_equal(errors, f"license status {relative}", item.get("LICENSE_STATUS"), expected_license)
        require_equal(errors, f"license file {relative}", item.get("LICENSE_FILE"), expected_file)
        if not (root / expected_file).is_file():
            errors.append(f"missing license text: {expected_file}")
    indexed = {item["PUBLIC_PATH"]: item for item in files}
    expected_external_sources = {
        pair for bindings in EXPECTED_SOURCES.values() for pair in bindings
    }
    actual_external_sources = {
        (source.get("SOURCE_PATH"), source.get("SOURCE_GIT_BLOB_OR_SHA256"))
        for item in files for source in item.get("SOURCES", [])
        if source.get("SOURCE_REVISION") == "498d4b25446003260d9367c10b1fdb27eb9988a1"
    }
    require_equal(errors, "complete 12-source authority set", actual_external_sources, expected_external_sources)
    require_equal(errors, "private archive source count", len(actual_external_sources), 12)
    for public_path, expected in EXPECTED_SOURCES.items():
        actual = [(source.get("SOURCE_PATH"), source.get("SOURCE_GIT_BLOB_OR_SHA256")) for source in indexed.get(public_path, {}).get("SOURCES", [])]
        require_equal(errors, f"source binding {public_path}", actual, expected)
    return len(files)


def verify_claims(root: Path, errors: list[str]) -> int:
    rows = load_csv(root, "provenance/claim_outcomes.csv")
    ids = [row["claim_id"] for row in rows]
    require_equal(errors, "claim count", len(rows), 31)
    require_equal(errors, "exact claim ID set", set(ids), set(EXPECTED_CLAIMS))
    if len(ids) != len(set(ids)):
        errors.append("duplicate claim_id")
    for row in rows:
        claim_id = row["claim_id"]
        if claim_id in EXPECTED_CLAIMS:
            actual = tuple(row[axis] for axis in AXES)
            require_equal(errors, f"canonical axes {claim_id}", actual, EXPECTED_CLAIMS[claim_id])
    return len(rows)


def verify_scientific_values(root: Path, errors: list[str]) -> None:
    clean = load_csv(root, "results/clean_detector/summary.csv")
    expected_clean = [
        ("calibration", "10", "10", "10", "10", "0", "0", "1.0000", "no"),
        ("held_out", "20", "20", "16", "20", "0", "4", "0.9000", "yes"),
        ("confirmatory", "30", "30", "24", "30", "0", "6", "0.9000", "yes"),
        ("pooled_secondary", "50", "50", "40", "50", "0", "10", "0.9000", "no"),
    ]
    actual_clean = [tuple(row[key] for key in ("stage", "positive_n", "control_n", "tp", "tn", "fp", "fn", "roc_auc", "independent_evaluation")) for row in clean]
    require_equal(errors, "clean detector values", actual_clean, expected_clean)

    transform = load_csv(root, "results/transformation_robustness/summary.csv")
    require_equal(errors, "transform values", [(r["condition"], r["positive_n"], r["control_n"], r["roc_auc"], r["outcome"]) for r in transform], [
        ("Clean", "30", "30", "1.0000", "INCONCLUSIVE"), ("Rot75", "30", "30", "0.9861", "INCONCLUSIVE"),
        ("JPEG25", "30", "30", "0.9978", "INCONCLUSIVE"), ("CropScale75", "30", "30", "0.8861", "INCONCLUSIVE"),
        ("Blur8", "30", "30", "0.9939", "INCONCLUSIVE"), ("Noise0.1", "30", "30", "0.6472", "INCONCLUSIVE"),
        ("Brightness6", "30", "30", "1.0000", "INCONCLUSIVE")])

    caption = load_csv(root, "results/caption_embedding/summary.csv")
    require_equal(errors, "caption values", [(r["configuration"], r["n"], r["mean_angular_gap_degrees"], r["median_angular_gap_degrees"], r["outcome"]) for r in caption], [
        ("none_clip", "1000", "9.3251", "9.5242", "REPRODUCED"),
        ("blip2_original", "1000", "44.5062", "45.1894", "REPRODUCED"),
        ("blip2_finetuned", "1000", "50.1505", "49.5758", "REPRODUCED")])
    require_equal(errors, "caption total N", sum(int(r["n"]) for r in caption), 3000)

    cat = load_csv(root, "results/cat_attack/summary.csv")
    require_equal(errors, "CAT primary values", [(r["track"], r["n"], r["roc_auc"], r["ci_low"], r["ci_high"], r["paper_target"], r["outcome"]) for r in cat[:3]], [
        ("basic_seal", "30", "0.7167", "0.6056", "0.8239", "0.551", "INCONCLUSIVE"),
        ("SOURCE_LITERAL_spatial", "30", "0.5450", "0.4633", "0.6378", "0.982", "INCONCLUSIVE"),
        ("PAPER_CONSISTENT_spatial", "30", "0.8011", "0.7150", "0.8878", "0.982", "INCONCLUSIVE")])
    require_equal(errors, "CAT localization findings", [cat[3]["limitation"], cat[4]["limitation"]], [
        "inside mean greater than outside in 21 of 30 attacked images", "inside mean greater than outside in 30 of 30 attacked images"])

    quality = json.loads((root / "results/generation_quality/summary.json").read_text(encoding="utf-8"))
    require_equal(errors, "generation quality", quality, {
        "claim_id": "GEN_QUALITY_SD_PROMPTS", "n_paired": 100, "metric": "SOURCE_DEFINED_CLIP_SCORE",
        "reproduction": {"before_mean": 32.5698, "after_mean": 33.3159, "paired_delta_mean": 0.7461, "paired_delta_median": 0.6994, "paired_delta_bootstrap_95_percentile_ci": [0.1876, 1.3111], "bootstrap_replicates": 10000},
        "paper_targets": {"before_mean": 32.378, "after_mean": 32.401, "delta": 0.023}, "outcome": "INCONCLUSIVE",
        "reason": "No paper-defined or pre-result numerical tolerance authorized an outcome decision."})

    semantic = json.loads((root / "results/semantic_angle/coverage.json").read_text(encoding="utf-8"))
    expected_semantic = {"claim_id": "SEMANTIC_ANGLE_EMPIRICAL_CURVE", "selected_records": 549, "configured_bins": 30, "populated_bins": 27,
        "empty_bin_ids": [1, 2, 3], "empty_intervals_degrees": ["[3,6)", "[6,9)", "[9,12)"], "minimum_observed_angle_degrees": 0.0,
        "maximum_observed_angle_degrees": 89.91099548339844, "outcome": "INCONCLUSIVE", "reason": "Publication mapping and comparison rule remain unresolved."}
    require_equal(errors, "semantic angle values", semantic, expected_semantic)


def verify_levels_sources_figures(root: Path, errors: list[str]) -> None:
    levels = load_csv(root, "provenance/reproducibility_levels.csv")
    require_equal(errors, "reproducibility entry count", len(levels), 32)
    require_equal(errors, "Level A count", sum(r["level"] == "A" for r in levels), 0)
    require_equal(errors, "Level B count", sum(r["level"] == "B" for r in levels), 8)
    require_equal(errors, "Level C count", sum(r["level"] == "C" for r in levels), 24)
    require_equal(errors, "reproducibility claim coverage", {r["claim_id"] for r in levels}, set(EXPECTED_CLAIMS) | {"SUPPORTING_CLEAN_DETECTOR"})

    versions = json.loads((root / "provenance/source_versions.json").read_text(encoding="utf-8"))
    expected_revisions = {
        "stable_diffusion": "4e63672c03103b6c636b8fb4119ba982469b2955", "caption_model": "0eb0d3b46c14c1f8c7680bca2693baafdb90bb28",
        "fine_tuned_sentence_embedding": "1f155d6a17f7a176d7d269f7ec04bcfa376ce297", "original_sentence_embedding": "6cc9279c672dc57f94445ef259b28a1b736fec8f",
        "clip": "3d74acf9a28c67741b2f4f2ea7635f0aaf6f0268", "prompt_dataset": "d816d4a05cb89bde39dd99284c459801e1e7e69a"}
    actual_revisions = {key: versions["verified_model_and_dataset_revisions"][key]["revision"] for key in expected_revisions}
    require_equal(errors, "model/data revisions", actual_revisions, expected_revisions)
    require_equal(errors, "COCO unresolved", versions["verified_model_and_dataset_revisions"]["coco_captions"]["status"], "UNRESOLVED")

    figure_text = {path: (root / path).read_text(encoding="utf-8") for path in ("figures/clean_detector.svg", "figures/transformation_robustness.svg", "figures/caption_embedding.svg")}
    for label in ("1.00", "0.90"):
        if label not in figure_text["figures/clean_detector.svg"]: errors.append(f"clean figure missing {label}")
    for label in ("1.0000", "0.9861", "0.9978", "0.8861", "0.9939", "0.6472"):
        if label not in figure_text["figures/transformation_robustness.svg"]: errors.append(f"transform figure missing {label}")
    for label in ("9.3251", "44.5062", "50.1505", "1,000/configuration"):
        if label not in figure_text["figures/caption_embedding.svg"]: errors.append(f"caption figure missing {label}")
    provenance = (root / "figures/README.md").read_text(encoding="utf-8")
    if "byte-exact figure renderer is **not** supplied" not in provenance:
        errors.append("figure provenance lacks byte-exact regeneration disclosure")


def verify(root: Path) -> list[str]:
    errors: list[str] = []
    verify_manifest(root, errors)
    verify_claims(root, errors)
    verify_scientific_values(root, errors)
    verify_levels_sources_figures(root, errors)
    for relative in ("scripts/build_manifest.py", "scripts/verify_release.py", "scripts/test_negative_mutations.py"):
        if "# SPDX-License-Identifier: MIT" not in (root / relative).read_text(encoding="utf-8"):
            errors.append(f"missing MIT script notice: {relative}")
    if not (root / "LICENSE_SCOPE.md").is_file():
        errors.append("missing scoped licensing notice")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    errors = verify(root)
    if errors:
        for error in errors: print(f"ERROR: {error}")
        raise SystemExit(1)
    print("PASS: full package hash coverage; exact 31-claim axes; 32 reproducibility entries; frozen values and authorities verified")


if __name__ == "__main__":
    main()
