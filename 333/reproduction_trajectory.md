# Reproduction Trajectory — Bug 333: pytorch-lightning

- **Bug report:** [https://github.com/Lightning-AI/pytorch-lightning/issues/21740](https://github.com/Lightning-AI/pytorch-lightning/issues/21740)
- **Repository:** Lightning-AI/pytorch-lightning @ `5f98958cb133c0b9e50831cc4f66ced2404c6729`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Read `bug_report.txt` and confirmed the issue concerns the `2.6.4` tag being force-pushed on GitHub.
2. Built a small repro script that checks the bundled snapshot version and probes for Git metadata.
3. Ran `bash run_repro.sh`; the run stops at the Git preflight because the bundled `codebase/` is not a Git repository.

## Observed behavior

- The report is about a GitHub tag being force-pushed. In this standardized folder, `codebase/src/version.info` reports 2.6.2 and `git -C codebase rev-parse --is-inside-work-tree` fails with `fatal: not a git repository`, so there is no local Git history to inspect or replay.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

This standardized folder does not include Git history or a remote repository checkout, so a tag-mutation issue on GitHub cannot be reproduced locally.
