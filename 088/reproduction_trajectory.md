# Reproduction Trajectory — Bug 088: x-transformers

- **Bug report:** [https://github.com/lucidrains/x-transformers/issues/290](https://github.com/lucidrains/x-transformers/issues/290)
- **Repository:** lucidrains/x-transformers @ `144d9ba84955139347e798ab025457b2d7adc314`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local virtualenv with setup_env.sh and installed torch, einops, einx, and packaging.
2. Ran repro.py through run_repro.sh.
3. Observed that align_right used 0 for left padding instead of the requested pad_id=9.

## Observed behavior

- Running repro.py produced aligned=[[0, 11, 12], [0, 0, 21]] while pad_id was 9, then raised AssertionError: align_right ignored pad_id.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
