# Reproduction Trajectory — Bug 460: pyro

- **Bug report:** [https://github.com/pyro-ppl/pyro/issues/3181](https://github.com/pyro-ppl/pyro/issues/3181)
- **Repository:** pyro-ppl/pyro @ `685c7adee65bbcdd6bd6c84c834a0a460f2224eb`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a clean Python 3.9 virtual environment from the bug folder.
2. Installed requirements from requirements.txt and the local codebase in editable mode.
3. Ran run_repro.sh, which executed the issue comparison from repro.py.
4. Observed that pyro_transformed.event_shape == torch_transformed.event_shape and no assertion failed.

## Observed behavior

- In a clean Python 3.9 venv with torch==1.13.1 and the local pyro commit 685c7ade, the issue snippet produced matching shapes: both TransformedDistribution instances had event_shape torch.Size([2]), and the equality assertion passed. See repro_stdout.log for the full run.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
VENV_DIR=$PWD/.venv_repro bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The mismatch described in the issue report does not occur in this checkout; the exact comparison passes, so there is no failing reproduction to capture.
