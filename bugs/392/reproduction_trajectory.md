# Reproduction Trajectory — Bug 392: lightning

- **Bug report:** [https://github.com/Lightning-AI/pytorch-lightning/issues/21689](https://github.com/Lightning-AI/pytorch-lightning/issues/21689)
- **Repository:** Lightning-AI/pytorch-lightning @ `0e20e15f2376f4f356470b08875639a945c43334`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Cloned Lightning-AI/pytorch-lightning at 0e20e15f2376f4f356470b08875639a945c43334 into codebase/
2. Inspected codebase/src/lightning/__init__.py and verified the import-time runtime hook is absent in the checked-out source
3. Ran bash run_repro.sh, which attempted pip download lightning==2.6.3 --no-deps and failed because the version is no longer available on the live index

## Observed behavior

- codebase/src/lightning/__init__.py does not contain the reported _runtime launcher or router_runtime.js reference
- run_repro.sh -> repro.py failed to download lightning==2.6.3: pip reported 'No matching distribution found for lightning==2.6.3'
- repro_stdout.log captures the clean source-tree check and the unavailable-wheel failure

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The exact lightning==2.6.3 wheel described in the report is no longer available from PyPI in this workspace, so the malicious archive cannot be downloaded and inspected here.
