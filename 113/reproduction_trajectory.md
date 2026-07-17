# Reproduction Trajectory — Bug 113: einops

- **Bug report:** [https://github.com/arogozhnikov/einops/issues/347](https://github.com/arogozhnikov/einops/issues/347)
- **Repository:** arogozhnikov/einops @ `1d3f9c4`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. bash setup_env.sh
2. bash run_repro.sh

## Observed behavior

- Running the repro in a local venv against the checked-out codebase shows the reported diagonal-style patterns are rejected. Examples from the captured output: `rearrange('ii->i')` raises `EinopsError` with `Identifiers only on one side of expression (should be on both): {'ii', 'i'}`; `reduce('ii->i', 'sum')` raises `EinopsError` with `Unexpected identifiers on the right side of reduce sum: {'i'}`. The repro script ends with `All reported diagonal patterns fail with EinopsError.`

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
