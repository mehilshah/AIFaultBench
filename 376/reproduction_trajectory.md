# Reproduction Trajectory — Bug 376: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/47059](https://github.com/huggingface/transformers/issues/47059)
- **Repository:** huggingface/transformers @ `b70d02fc724d04c916832ca4ead03ff05e8fb1ee`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a local virtual environment with `bash setup_env.sh`.
2. Run `bash run_repro.sh` or `python3 repro.py` from the bug folder.
3. Observe the AttributeError stack trace in `repro_stderr.log`.

## Observed behavior

- Running `bash run_repro.sh` in a fresh local venv with `huggingface_hub==1.22.0`, `typer==0.26.8`, and `click==8.4.2` prints the expected version preamble and then fails with `AttributeError: 'HFCliTyperGroup' object has no attribute '_add_completion'` from `typer/testing.py` -> `typer/main.py::get_command` when `CliRunner.invoke(transformers_cli.app, ["version"], catch_exceptions=False)` is executed.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
