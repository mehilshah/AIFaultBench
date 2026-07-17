# Reproduction Trajectory — Bug 402: SDV

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2825](https://github.com/sdv-dev/SDV/issues/2825)
- **Repository:** sdv-dev/SDV @ `b895858c1e306b64f5debf7adc78bdb2b9c78131`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. bash setup_env.sh
2. bash run_repro.sh

## Observed behavior

- Running the reproduced setup against commit b895858c1e306b64f5debf7adc78bdb2b9c78131 fails immediately at Metadata.set_primary_key(['user_id', 'user_id'], table_name='accounts') with sdv.metadata.errors.InvalidMetadataError: 'primary_key' must be a string. The reported AttributeError: 'DataFrame' object has no attribute 'dtype' does not occur in this checkout.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```

## Why it does not reproduce on the reference machine

This source snapshot already validates primary_key as a string before the duplicate-column path can reach the buggy fit-time code, so the issue described in the report is not reachable here.
