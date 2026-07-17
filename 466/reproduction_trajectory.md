# Reproduction Trajectory — Bug 466: pytorch-lightning

- **Bug report:** [https://github.com/Lightning-AI/pytorch-lightning/issues/21576](https://github.com/Lightning-AI/pytorch-lightning/issues/21576)
- **Repository:** Lightning-AI/pytorch-lightning @ `c05cadbe5be3bfa8bacbd9d7e912fa2e456413ff`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Checked out the referenced Lightning commit into `codebase/`.
2. Created a minimal repro checker in `repro.py` and wrappers in `run_repro.sh` and `setup_env.sh`.
3. Ran `bash run_repro.sh` and verified the script reported `reproducible=false` with no `@Blaizzy` match.

## Observed behavior

- Running `bash run_repro.sh` on Lightning commit c05cadbe5be3bfa8bacbd9d7e912fa2e456413ff found no local `@Blaizzy` or `Blaizzy` reference in the checked-out repo. The only nearby tag mentions are unrelated `@ethanwharris` entries in `.github/CODEOWNERS`, `.github/workflows/release-pkg.yml`, and `docs/source-pytorch/community/governance.rst`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

This report is a GitHub tagging/notification request rather than an executable product bug, and the local checkout does not contain the reported `@Blaizzy` mention.
