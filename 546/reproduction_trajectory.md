# Reproduction Trajectory — Bug 546: accelerate

- **Bug report:** [https://github.com/huggingface/accelerate/issues/1116](https://github.com/huggingface/accelerate/issues/1116)
- **Repository:** huggingface/accelerate @ `907a86d145cc62521ea0281eb24465f537480e2d`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a multi-GPU config with num_machines=2 and gpu_ids=0.
2. Run accelerate launch control flow with launcher functions monkeypatched to record the chosen branch.
3. Repeat with gpu_ids=all as a control.

## Observed behavior

- gpu_ids=0 -> selected=simple_launcher multi_gpu=False num_machines=2 gpu_ids=0
- gpu_ids=all -> selected=multi_gpu_launcher multi_gpu=True num_machines=2 gpu_ids=all

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
