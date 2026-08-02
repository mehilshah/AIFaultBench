# Reproduction Trajectory — Bug 666: smolagents

- **Bug report:** [https://github.com/huggingface/smolagents/issues/2073](https://github.com/huggingface/smolagents/issues/2073)
- **Repository:** huggingface/smolagents @ `5c684c18df01895832ed0e0caecb6896f72890da`
- **Outcome:** Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and confirmed the checkout resolved to the pinned commit.
2. Created `.venv`, installed the exact pinned runtime dependencies, and installed the checkout editable.
3. Ran `repro.py`, which creates a temporary user script named `smolagents.py` containing the import from the report and executes it in that directory.
4. Asserted that the child exits non-zero and its traceback says the locally named `smolagents` module is partially initialized.

## Observed behavior

- `bash run_repro.sh` exited with status 1.
- The harness printed `OBSERVED: ImportError: cannot import name 'OpenAIServerModel' from partially initialized module 'smolagents'`.
- The child traceback named the temporary local `smolagents.py`, demonstrating Python's module-shadowing behavior. No model or provider client was constructed.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
