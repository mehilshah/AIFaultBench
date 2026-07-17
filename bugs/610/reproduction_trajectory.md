# Reproduction Trajectory — Bug 610: pytorch-lightning

- **Bug report:** [https://github.com/Lightning-AI/pytorch-lightning/issues/21435](https://github.com/Lightning-AI/pytorch-lightning/issues/21435)
- **Repository:** Lightning-AI/pytorch-lightning @ `2e25642a6fe33b23c524884bbf40213336d57126`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an isolated venv and installed the runtime dependencies from requirements.txt.
2. Imported the local codebase from codebase/src and instantiated MixedPrecision(precision='bf16-mixed', device='cpu').
3. Created torch.optim.AdamW(..., fused=True) and called precision.clip_gradients(optimizer, clip_val=1.0).
4. Observed the reported RuntimeError in the local snapshot.

## Observed behavior

- Local snapshot reports lightning_version=2.6.0.
- repro.py prints scaler_is_none=True and optimizer_type=AdamW with step_supports_amp_scaling=True.
- The run ends with RuntimeError: The current optimizer, AdamW, does not allow for gradient clipping because it performs unscaling of gradients internally. HINT: Are you using a 'fused' optimizer?

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
