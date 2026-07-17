# Reproduction Trajectory — Bug 570: diffusers

- **Bug report:** [https://github.com/huggingface/diffusers/issues/13696](https://github.com/huggingface/diffusers/issues/13696)
- **Repository:** huggingface/diffusers @ `4ca863323d550842e7d0122efd57d84d9b75d1cf`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local CPU-compatible venv and installed torch plus the diffusers source snapshot from codebase/.
2. Ran `bash run_repro.sh`, which launches a 2-process distributed QwenImageTransformer2DModel comparison with a non-contiguous encoder_hidden_states_mask.
3. Observed a mismatch between Ulysses context-parallel output and the non-SP baseline, with torch.testing.assert_close raising an AssertionError.

## Observed behavior

- In the bundled CPU/gloo repro, the SP and non-SP outputs diverge: max_abs_diff=0.022140145301818848 with 30 / 512 mismatched elements, and torch.testing.assert_close fails at rtol=1e-2, atol=1e-2.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
