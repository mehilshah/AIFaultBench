# Reproduction Trajectory — Bug 176: lark

- **Bug report:** [https://github.com/lark-parser/lark/issues/1434](https://github.com/lark-parser/lark/issues/1434)
- **Repository:** lark-parser/lark @ `5016894`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local virtual environment and installed the editable codebase from ./codebase.
2. Ran the exact grammar from the bug report in fresh subprocesses 40 times.
3. Observed four different parse trees for the same input string a.?

## Observed behavior

- Running the exact grammar in 40 fresh Python subprocesses produced 4 distinct parse trees. The successful run reported: unique_trees=4, with counts 8, 6, 13, and 13 across the four tree shapes. This shows the parse result is non-deterministic across processes in the local codebase.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
