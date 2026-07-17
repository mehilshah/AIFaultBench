# Reproduction Trajectory — Bug 086: x-transformers

- **Bug report:** [https://github.com/lucidrains/x-transformers/issues/305](https://github.com/lucidrains/x-transformers/issues/305)
- **Repository:** lucidrains/x-transformers @ `cdf51f7127d2af478030b81c44d7a1ddb35716a8`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a virtual environment and installed the dependencies from requirements.txt.
2. Ran bash run_repro.sh, which executes repro.py against the local codebase.
3. Observed the exact EinopsError from RotaryEmbedding.forward() when use_xpos=True.

## Observed behavior

- Running bash run_repro.sh on Python 3.12.3 with torch 2.13.0+cu130 reproduced the reported rotary XPos failure. repro_stderr.log shows einops.EinopsError: Error while processing rearrange-reduction pattern "n -> n 1" with input tensor shape torch.Size([1, 32]) and the failure originates at codebase/x_transformers/x_transformers.py:669.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
