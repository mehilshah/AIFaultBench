# Reproduction Trajectory — Bug 316: diffusers

- **Bug report:** [https://github.com/huggingface/diffusers/issues/14114](https://github.com/huggingface/diffusers/issues/14114)
- **Repository:** huggingface/diffusers @ `72eb60c2dad62e44777b5344f21705c6d47bf97f`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a CPU-safe stub for the `_flash_3_varlen_hub` kernel that preserves the backend's packed-prefix slicing behavior.
2. Ran the backend on a contiguous all-ones mask and confirmed it matches the masked reference implementation.
3. Ran the backend on a non-contiguous mask with holes and compared both forward output and gradients against the reference implementation.

## Observed behavior

- Contiguous mask matched the reference path: forward_max_abs_diff=0.000000 and grad_max_abs_diff=0.000000.
- Non-contiguous mask diverged from the reference path: forward_max_abs_diff=8.000122 and grad_max_abs_diff=24516.000000.
- The repro terminated with AssertionError: Tensor-likes are not close!

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
