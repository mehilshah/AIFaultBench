# Reproduction Trajectory — Bug 513: accelerate

- **Bug report:** [https://github.com/huggingface/accelerate/issues/1183](https://github.com/huggingface/accelerate/issues/1183)
- **Repository:** huggingface/accelerate @ `37831808444e089a182f66713935d27c39a0cf2c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a clean .venv and installed the local accelerate snapshot from codebase/ with the repro dependencies.
2. Ran bash run_repro.sh, which launches 4 CPU distributed workers and exercises Accelerator.main_process_first() and Accelerator.local_main_process_first().
3. Observed out-of-order execution: non-main ranks printed before rank 0, and the shared ordered_results list confirmed the misordering.

## Observed behavior

- In repro_stdout.log, the first recorded main-process event is rank 1, not rank 0: ordered_results starts with [('main', 1, False), ('main', 3, False), ('main', 2, False), ('main', 0, True), ...]. The repro then raises RuntimeError with 'main_process_first/local_main_process_first misordered'.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
