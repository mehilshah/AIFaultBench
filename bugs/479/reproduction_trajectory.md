# Reproduction Trajectory — Bug 479: diffusers

- **Bug report:** [https://github.com/huggingface/diffusers/issues/13866](https://github.com/huggingface/diffusers/issues/13866)
- **Repository:** huggingface/diffusers @ `25b85c1d0b18adf0271fb9f4b547aea244a889ca`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an isolated Python environment with `setup_env.sh`.
2. Executed `bash run_repro.sh` against the reproduced batching logic from `examples/dreambooth/train_dreambooth_lora_flux2_klein_img2img.py`.
3. Observed that the same conditioning-image shape in the same batch generated different time coordinates instead of repeating a single reference ID block.

## Observed behavior

- Running `bash run_repro.sh` reproduced the batching issue: two identical conditioning images produced different image IDs after the batch split. The first batch element matched the single-image reference, but the second did not (`batch0_equals_reference=true`, `batch1_equals_reference=false`, `batch0_equals_batch1=false`). The captured output shows `T=10` for batch 0 and `T=20` for batch 1 even though the images are identical.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
