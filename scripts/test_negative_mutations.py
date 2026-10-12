#!/usr/bin/env python3
"""Prove that reviewed package mutations are rejected by verify_release.py."""

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


def expect_rejection(name: str, mutate) -> None:
    temp, root = candidate()
    try:
        mutate(root)
        result = run([sys.executable, "scripts/verify_release.py", "--root", str(root)], root)
        if result.returncode == 0:
            raise SystemExit(f"FAIL: mutation accepted: {name}")
        print(f"PASS: rejected {name}")
    finally:
        temp.cleanup()


def main() -> None:
    cases = [
        ("non-evaluated claim ID", lambda root: replace(root, "provenance/claim_outcomes.csv", "PATCH_L2_SEED_DISCRIMINATION", "PATCH_L2_CHANGED")),
        ("canonical non-evaluated axis", lambda root: replace(root, "provenance/claim_outcomes.csv", "PATCH_L2_SEED_DISCRIMINATION,BLOCKED", "PATCH_L2_SEED_DISCRIMINATION,NON_EVALUABLE")),
        ("scientific summary value", lambda root: replace(root, "results/caption_embedding/summary.csv", "50.1505", "50.1506")),
        ("source authority binding", lambda root: replace(root, "provenance/artifact_manifest.json", "bdd95c871cf2294fa300c75cade1b62c3529c2a5", "0000000000000000000000000000000000000000")),
        ("unmanifested tracked file", lambda root: ((root / "unexpected.txt").write_text("unexpected\n", encoding="utf-8"), subprocess.run(["git", "add", "unexpected.txt"], cwd=root, check=True))),
    ]
    for name, mutation in cases:
        expect_rejection(name, mutation)
    print(f"PASS: {len(cases)}/{len(cases)} negative mutation cases rejected")


if __name__ == "__main__":
    main()
