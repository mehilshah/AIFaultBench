# Reproduction Trajectory — Bug 175: lark

- **Bug report:** [https://github.com/lark-parser/lark/issues/1416](https://github.com/lark-parser/lark/issues/1416)
- **Repository:** lark-parser/lark @ `53c3964`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local venv with `bash setup_env.sh` and installed the editable local `codebase/` checkout.
2. Ran `bash run_repro.sh`, which executes `repro.py` against the local Lark checkout.
3. Observed that `Lark(..., transformer=MyTransformer())` returned `Token('NUMBER', '1.0')` instead of `ACOS called with argument: 1.0`.

## Observed behavior

- Running `bash run_repro.sh` exits with code 1. stdout shows `result_type=Token`, `result_repr=Token('NUMBER', '1.0')`, and `result_str=1.0`, while stderr ends with `AssertionError: Transformer callback was not applied`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
