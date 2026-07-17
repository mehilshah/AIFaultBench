# Reproduction Trajectory — Bug 512: pytorch-lightning

- **Bug report:** [https://github.com/Lightning-AI/pytorch-lightning/issues/21556](https://github.com/Lightning-AI/pytorch-lightning/issues/21556)
- **Repository:** Lightning-AI/pytorch-lightning @ `8d86b2417d56703d5cc4f0da76acc71717d1dab7`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a clean Python venv and installed a CPU-only torch plus the minimal Lightning Fabric runtime dependencies.
2. Loaded the checked-in Lightning source from codebase/src while bypassing the top-level lightning package import path.
3. Instantiated FSDPPrecision("bf16-mixed") and created a module inside module_init_context().
4. Observed the initialized parameter dtype was torch.bfloat16 instead of the expected torch.float32, which triggered the assertion.

## Observed behavior

- repro_stdout.log shows expected_dtype=torch.float32 and actual_dtype=torch.bfloat16; repro_stderr.log shows AssertionError: Expected module init to keep parameters in torch.float32, got torch.bfloat16.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
