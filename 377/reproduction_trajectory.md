# Reproduction Trajectory — Bug 377: diffusers

- **Bug report:** [https://github.com/huggingface/diffusers/issues/13999](https://github.com/huggingface/diffusers/issues/13999)
- **Repository:** huggingface/diffusers @ `7bf00006aa005eae37bcc639fd0f010c183365b4`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a fresh Python venv and install CPU Torch plus the minimal Diffusers runtime dependencies.
2. Run repro.py in auto mode via run_repro.sh on this CPU-only machine.
3. Observe that _flash_attention_3_varlen_hub unpacks a tensor return as if it were a tuple and truncates the output.

## Observed behavior

- run_repro.sh completed in a clean venv and the mock FA3 varlen path printed: expected shape (2, 4, 2, 64), actual shape (2, 1, 64), actual tensor equals expected: False, followed by 'BUG REPRODUCED: tensor return was destructured as if it were a tuple.'

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
