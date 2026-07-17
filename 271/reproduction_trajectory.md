# Reproduction Trajectory — Bug 271: DeepSpeed

- **Bug report:** [https://github.com/deepspeedai/DeepSpeed/issues/8072](https://github.com/deepspeedai/DeepSpeed/issues/8072)
- **Repository:** microsoft/DeepSpeed @ `ad026a1fd1239071f2afb0a9c07f04b3cd732e02`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a minimal repro that mirrors deepspeed/runtime/zero/partition_parameters.py using a bf16 base tensor followed by a fp32 adapter tensor.
2. Installed the runtime into a local venv with setup_env.sh.
3. Ran ./run_repro.sh and observed the TypeError from the mixed-dtype all-gather path.

## Observed behavior

- Running ./run_repro.sh exits 1. repro_stdout.log shows the bf16 base parameter and fp32 LoRA parameter, then reports: "output tensor must have the same type as input tensor".

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
