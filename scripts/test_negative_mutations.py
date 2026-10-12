#!/usr/bin/env python3
"""Prove scientific guards reject mutations after applicable hashes are refreshed."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1]


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, capture_output=True, text=True)


def candidate() -> tuple[tempfile.TemporaryDirectory[str], Path]:
    temp = tempfile.TemporaryDirectory(prefix="seal-release-negative-")
    root = Path(temp.name) / "candidate"
    shutil.copytree(SOURCE, root, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root, check=True)
    subprocess.run(["git", "add", "--all"], cwd=root, check=True)
    return temp, root


def replace(root: Path, relative: str, old: str, new: str) -> None:
    path = root / relative
    content = path.read_text(encoding="utf-8")
    if old not in content:
        raise RuntimeError(f"mutation target absent: {relative}: {old}")
    path.write_text(content.replace(old, new, 1), encoding="utf-8", newline="\n")


def regenerate_manifest(root: Path) -> None:
    result = run([sys.executable, "scripts/build_manifest.py"], root)
    if result.returncode != 0:
        raise RuntimeError(f"manifest regeneration failed: {result.stderr}")


def expect_rejection(name: str, expected_reason: str, mutate, regenerate: bool = True) -> None:
    temp, root = candidate()
    try:
        mutate(root)
        if regenerate:
            regenerate_manifest(root)
        result = run([sys.executable, "scripts/verify_release.py", "--root", str(root)], root)
        combined = result.stdout + result.stderr
        if result.returncode == 0:
            raise SystemExit(f"FAIL: mutation accepted: {name}")
        if expected_reason not in combined:
            raise SystemExit(f"FAIL: {name} rejected for wrong reason; expected {expected_reason!r}; output={combined!r}")
        if "hash mismatch" in combined:
            raise SystemExit(f"FAIL: {name} relied on stale package hash")
        print(f"PASS: rejected {name} via {expected_reason}")
    finally:
        temp.cleanup()


def main() -> None:
    cases = [
        ("non-evaluated claim ID", "exact claim ID set", lambda root: replace(root, "provenance/claim_outcomes.csv", "PATCH_L2_SEED_DISCRIMINATION", "PATCH_L2_CHANGED"), True),
        ("canonical non-evaluated axis", "canonical axes PATCH_L2_SEED_DISCRIMINATION", lambda root: replace(root, "provenance/claim_outcomes.csv", "PATCH_L2_SEED_DISCRIMINATION,BLOCKED", "PATCH_L2_SEED_DISCRIMINATION,NON_EVALUABLE"), True),
        ("scientific summary value", "caption values", lambda root: replace(root, "results/caption_embedding/summary.csv", "50.1505", "50.1506"), True),
        ("source authority binding", "complete 12-source authority set", lambda root: replace(root, "scripts/build_manifest.py", "bdd95c871cf2294fa300c75cade1b62c3529c2a5", "0000000000000000000000000000000000000000"), True),
        ("unmanifested tracked file", "manifest path set", lambda root: ((root / "unexpected.txt").write_text("unexpected\n", encoding="utf-8"), subprocess.run(["git", "add", "unexpected.txt"], cwd=root, check=True)), False),
    ]
    for name, reason, mutation, regenerate in cases:
        expect_rejection(name, reason, mutation, regenerate)
    print(f"PASS: {len(cases)}/{len(cases)} negative mutation cases rejected by intended guards")


if __name__ == "__main__":
    main()
