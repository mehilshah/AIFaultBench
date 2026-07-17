# Reproduction Trajectory — Bug 418: pytorch_geometric

- **Bug report:** [https://github.com/pyg-team/pytorch_geometric/issues/10163](https://github.com/pyg-team/pytorch_geometric/issues/10163)
- **Repository:** pyg-team/pytorch_geometric @ `69193c895fe721fb45e63985bb79e8d130ee7782`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Inspected bug_report.txt and the pinned TransformerConv source snapshot under codebase/.
2. Set up an isolated Python environment with torch==2.5.1 and torch-geometric==2.6.1.
3. Ran the repro script and observed the expected assertion failure showing the bias mismatch.

## Observed behavior

- run_repro.sh created a clean venv, installed torch==2.5.1 and torch-geometric==2.6.1, and executed repro.py successfully up to the assertion.
- repro.py printed: lin_key_bias_is_none=false, lin_query_bias_is_none=false, lin_value_bias_is_none=false, lin_skip_bias_is_none=true.
- repro.py terminated with AssertionError: bias=False is not respected by TransformerConv: lin_key, lin_query, and lin_value still have bias parameters.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
