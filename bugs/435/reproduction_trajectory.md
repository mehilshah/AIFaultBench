# Reproduction Trajectory — Bug 435: diffusers

- **Bug report:** [https://github.com/huggingface/diffusers/issues/13930](https://github.com/huggingface/diffusers/issues/13930)
- **Repository:** huggingface/diffusers @ `41add3410424cc33d748a7fd3409132d2f6b4ad2`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Restored the referenced diffusers checkout at commit 41add3410424cc33d748a7fd3409132d2f6b4ad2.
2. Created a CPU-only torch environment with setup_env.sh.
3. Ran bash run_repro.sh, which exercised the toy connector layout from the bug report and failed on the mismatch.

## Observed behavior

- repro_stdout.log prints the issue's mismatched sequences: reference [1.0, 2.0, 3.0, 3.0, 0.0, 1.0, 2.0, 3.0] vs current [3.0, 2.0, 1.0, 0.0, 3.0, 2.0, 1.0, 0.0]
- repro_stderr.log ends with AssertionError: layout mismatch: current diffusers behavior reverses prompt tokens and registers

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
