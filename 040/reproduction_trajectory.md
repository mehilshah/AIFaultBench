# Reproduction Trajectory — Bug 040: annotated_deep_learning_paper_implementations

- **Bug report:** [https://github.com/labmlai/annotated_deep_learning_paper_implementations/issues/146](https://github.com/labmlai/annotated_deep_learning_paper_implementations/issues/146)
- **Repository:** labmlai/annotated_deep_learning_paper_implementations @ `05632f9f8e0de4657c210a13954a81f9556fd1ed`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Load the actual DDPM AttentionBlock implementation from the bundled codebase.
2. Construct deterministic q, k, v tensors from the module's projection layer.
3. Compare softmax(dim=1) against the expected softmax(dim=2) normalization axis.

## Observed behavior

- codebase/labml_nn/diffusion/ddpm/unet.py:188 uses attn.softmax(dim=1) after einsum('bihd,bjhd->bijh', ...).
- Buggy attention sum over query axis max deviation: 1.192e-07.
- Buggy attention sum over key axis max deviation: 3.868e+00.
- Correct attention sum over key axis max deviation: 1.192e-07.
- Max absolute difference between buggy and corrected attention weights: 6.674e-01.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
