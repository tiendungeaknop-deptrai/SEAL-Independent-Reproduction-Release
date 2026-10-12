#!/usr/bin/env python3
"""Verify curated release hashes and frozen 31-claim scientific state."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_EVALUATED = {
    "TRANSFORM_ROBUSTNESS": "INCONCLUSIVE",
    "CAT_ATTACK_BASIC_AUC": "INCONCLUSIVE",
    "CAT_ATTACK_SPATIAL_AUC": "INCONCLUSIVE",
    "CAT_ATTACK_LOCALIZATION_SIGNAL": "INCONCLUSIVE",
    "EMBEDDING_ABLATION": "REPRODUCED",
    "GEN_QUALITY_SD_PROMPTS": "INCONCLUSIVE",
    "SEMANTIC_ANGLE_EMPIRICAL_CURVE": "INCONCLUSIVE",
}
STATES = {"EVALUATED", "BLOCKED", "DIAGNOSTIC_ONLY", "NON_EVALUABLE"}
OUTCOMES = {"REPRODUCED", "PARTIALLY_REPRODUCED", "NOT_REPRODUCED", "INCONCLUSIVE", "NONE"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_manifest(errors: list[str]) -> int:
    manifest = json.loads((ROOT / "provenance/artifact_manifest.json").read_text(encoding="utf-8"))
    artifacts = manifest.get("artifacts", [])
    if manifest.get("artifact_count") != len(artifacts):
        errors.append("manifest artifact_count mismatch")
    seen = set()
    for item in artifacts:
        rel = item["PUBLIC_PATH"]
        if rel in seen:
            errors.append(f"duplicate manifest path: {rel}")
        seen.add(rel)
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"missing artifact: {rel}")
        elif sha256(path) != item["RELEASED_SHA256"]:
            errors.append(f"hash mismatch: {rel}")
    return len(artifacts)


def verify_claims(errors: list[str]) -> int:
    with (ROOT / "provenance/claim_outcomes.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    ids = [row["claim_id"] for row in rows]
    if len(rows) != 31:
        errors.append(f"expected 31 claims, found {len(rows)}")
    if len(ids) != len(set(ids)):
        errors.append("duplicate claim_id")
    for row in rows:
        if row["resolution_state"] not in STATES:
            errors.append(f"invalid state for {row['claim_id']}")
        if row["outcome"] not in OUTCOMES:
            errors.append(f"invalid outcome for {row['claim_id']}")
        if row["finality"] != "FINAL":
            errors.append(f"non-final claim: {row['claim_id']}")
        if row["resolution_state"] == "BLOCKED" and row["outcome"] != "NONE":
            errors.append(f"blocked claim has non-NONE outcome: {row['claim_id']}")
    actual = {row["claim_id"]: row["outcome"] for row in rows if row["claim_id"] in EXPECTED_EVALUATED}
    if actual != EXPECTED_EVALUATED:
        errors.append(f"evaluated outcome mismatch: {actual}")
    return len(rows)


def main() -> None:
    errors: list[str] = []
    artifact_count = verify_manifest(errors)
    claim_count = verify_claims(errors)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print(f"PASS: {artifact_count} manifested artifacts; {claim_count}/31 final claims; frozen outcomes preserved")


if __name__ == "__main__":
    main()

