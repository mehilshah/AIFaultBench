# Reproduction Trajectory — Bug 531: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/46832](https://github.com/huggingface/transformers/issues/46832)
- **Repository:** huggingface/transformers @ `4d47b06102805e02662d5d9865994bed8aa6d7fb`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local virtual environment and installed the minimal runtime dependencies from requirements.txt.
2. Ran repro.py through run_repro.sh with RTDetrConfig(num_feature_levels=4, num_labels=80, image_size=640).
3. Observed the TypeError in RTDetrModel.forward at the decoder_input_proj extra-level branch.
4. Verified the default RT-DETR control case with num_feature_levels=3 completes successfully.

## Observed behavior

- Running ./run_repro.sh in an isolated venv with torch 2.5.1+cpu and the local codebase reproduces the reported TypeError: conv2d() received a list instead of a Tensor at codebase/src/transformers/models/rt_detr/modeling_rt_detr.py:1626. The same script also confirms the default num_feature_levels=3 control path passes.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./setup_env.sh && ./run_repro.sh
```
