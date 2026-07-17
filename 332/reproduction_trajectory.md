# Reproduction Trajectory — Bug 332: diffusers

- **Bug report:** [https://github.com/huggingface/diffusers/issues/14103](https://github.com/huggingface/diffusers/issues/14103)
- **Repository:** huggingface/diffusers @ `26ec30e8add5faec242aed6a4bfe0d23a6e9befd`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Create a clean Python 3.12 virtualenv and install the pinned dependencies from requirements.txt.
2. Set PYTHONPATH to codebase/src and run repro.py through run_repro.sh.
3. Compare the attn2 processor mapping before and after one UNet2DConditionModel forward pass.

## Observed behavior

- In the bundled run, every attn2 processor stayed as IPAdapterWrapper before and after the forward pass, the module-level processor remained IPAdapterWrapper, and the wrapper executed 4 times. See repro_stdout.log.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./setup_env.sh && ./run_repro.sh
```

## Why it does not reproduce on the reference machine

The reported processor overwrite does not occur in this checkout; the injected custom wrapper is preserved across the forward pass.
