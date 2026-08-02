# Reproduction Trajectory — Bug 716: SWE-agent

- **Bug report:** [https://github.com/SWE-agent/SWE-agent/issues/1078](https://github.com/SWE-agent/SWE-agent/issues/1078)
- **Repository:** SWE-agent/SWE-agent @ `aa4e8ea1611dad2220950cc5afb30aff17932b41`
- **Outcome:** Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`, then explicitly fetched and checked out the pinned commit because the initial clone had no checked-out commit.
2. Inspected `sweagent/run/hooks/open_pr.py` and confirmed that `open_pr` appends the complete formatted trajectory to `body` without a size limit.
3. Created `repro.py`, which loads that pinned source file, replaces every external collaborator with local doubles, and supplies a single 65,536-character observation.
4. Ran `bash run_repro.sh`; the fake GitHub PR endpoint applied GitHub's 65,536-character body limit and rejected the body forwarded by the unmodified hook.

## Observed behavior

- `run_repro.sh` exited with status 1.
- The pinned hook sent a 65,874-character PR body and the offline endpoint raised: `HTTP 422: body is too long (maximum is 65536 characters); got 65874`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
