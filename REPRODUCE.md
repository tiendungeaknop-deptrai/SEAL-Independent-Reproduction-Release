# Verification and reproduction guide

## What can be verified locally

Requires Python 3.10 or newer and only the standard library.

```bash
python scripts/verify_release.py
```

The command checks the full non-circular SHA-256 manifest, the exact 31-claim identity set and all five canonical axes, fixed scientific summary values, twelve archive authority bindings, 32 reproducibility entries, and scoped license metadata. A successful run verifies this package; it does not recompute scientific metrics from per-record observations.

## What cannot be replayed from this package

All released scientific results are Level B or C. Record-level image/model outputs and some required third-party inputs remain in a private archive or are not redistributable. The package therefore does not claim a public end-to-end model rerun or statistic recomputation.

To independently reconstruct an experiment, retrieve the upstream source at commit `92d31b31b93a6e373fe88a584c640beafb68c6fa`, follow `docs/experimental_protocols.md`, independently obtain all licensed models and datasets, and document every deviation. The private archive locators in the manifest are provenance identifiers, not public download promises.

## Determinism

The release verifier is deterministic over repository bytes. Scientific generation is not executed by it. No fake inputs or generated substitute observations are provided.

