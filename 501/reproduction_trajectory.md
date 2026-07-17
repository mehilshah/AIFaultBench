# Reproduction Trajectory — Bug 501: DeepSpeed

- **Bug report:** [https://github.com/deepspeedai/DeepSpeed/issues/7773](https://github.com/deepspeedai/DeepSpeed/issues/7773)
- **Repository:** microsoft/DeepSpeed @ `8a9369d03e800e413a31503ceb0e5d39e390d845`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a fresh Python 3.12 virtualenv and installed the CPU torch wheel plus the minimal DeepSpeed Python dependencies.
2. Ran a one-stage PipelineModule with the same 8-sample global batch under gradient_accumulation_steps=1 and gradient_accumulation_steps=4.
3. Captured the custom optimizer's pre-step gradient norm for both runs and compared the results.

## Observed behavior

- On a clean CPU torch 2.9.1+cpu install with DS_ACCELERATOR=cpu, a one-stage PipelineModule produced identical outputs for GAS=1 and GAS=4: gas1_norm=10.010870933532715, gas4_norm=10.010870933532715, ratio=1.0.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The reported gradient-summing behavior did not reproduce in this checkout; the two runs matched exactly, so there is no failing case to isolate here.
