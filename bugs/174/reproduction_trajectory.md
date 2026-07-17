# Reproduction Trajectory — Bug 174: lark

- **Bug report:** [https://github.com/lark-parser/lark/issues/1355](https://github.com/lark-parser/lark/issues/1355)
- **Repository:** lark-parser/lark @ `44483c9`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local virtual environment with `bash setup_env.sh` and installed the editable `codebase/` snapshot as `lark 1.1.7`.
2. Executed `bash run_repro.sh`, which runs `repro.py` against the issue grammar.
3. Observed `GrammarError` on the alias name `mask`, confirming the bug reproduces in this folder.

## Observed behavior

- Running `bash run_repro.sh` exits with status 1.
- The captured stdout shows `lark version: 1.1.7`, then `GrammarError` and `Rule 'mask' used but not defined (in rule pipesyn)`.
- The grammar from the report is loaded directly from `repro.py`, so the undefined-rule error is triggered by the reported input.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
