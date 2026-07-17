# Reproduction Trajectory — Bug 393: accelerate

- **Bug report:** [https://github.com/huggingface/accelerate/issues/1573](https://github.com/huggingface/accelerate/issues/1573)
- **Repository:** huggingface/accelerate @ `665d5180fcc01d5700f7a9aa3f9bdb75c6055dce`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create an isolated venv and install the pinned CPU-only dependencies.
2. Run the 4-process CPU distributed harness in repro.py.
3. Observe the assertion failure from test_split_between_processes_nested_dict on ranks 1-3.

## Observed behavior

- Nested-dict split assertion fails in a 4-process run at accelerate/test_utils/scripts/test_script.py:479: assert results["a"] == data_copy["a"][-1]

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
