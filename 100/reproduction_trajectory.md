# Reproduction Trajectory — Bug 100: rotary-embedding-torch

- **Bug report:** [https://github.com/lucidrains/rotary-embedding-torch/issues/18](https://github.com/lucidrains/rotary-embedding-torch/issues/18)
- **Repository:** lucidrains/rotary-embedding-torch @ `2da4a529854ba272535e40193177ee906ce1961b`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a Python virtual environment and installed the package dependencies from requirements.txt.
2. Ran repro.py through run_repro.sh against the local codebase/ copy.
3. Verified that the second backward pass succeeded while reusing the cached frequencies.

## Observed behavior

- The two-iteration training loop completed without raising RuntimeError.
- After the first iteration, cached_freqs existed and cached_freqs.grad_fn was None.
- The saved stdout shows step=0, step=1, and result=not_reproduced.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The checked-in code already avoids caching trainable frequencies, so the reported autograd reuse error does not occur in this snapshot.
