# Reproduction Trajectory — Bug 484: diffusers

- **Bug report:** [https://github.com/huggingface/diffusers/issues/13864](https://github.com/huggingface/diffusers/issues/13864)
- **Repository:** huggingface/diffusers @ `3e83f4348f0c6baea8bee3d1ff7676f50e11e74c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Read the bug report and identified that the failing path is the Cosmos pipeline's text-safety check.
2. Verified the source line in `codebase/src/diffusers/pipelines/cosmos/pipeline_cosmos2_5_predict.py` that calls `self.safety_checker.check_text_safety(p)`.
3. Ran the minimal repro with a pipeline object assigned to `safety_checker` and observed the reported `AttributeError`.

## Observed behavior

- Running `bash run_repro.sh` prints `verified source marker: codebase/src/diffusers/pipelines/cosmos/pipeline_cosmos2_5_predict.py:677` and then fails with `AttributeError: 'Cosmos2_5_PredictBasePipeline' object has no attribute 'check_text_safety'`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
