# Reproduction Trajectory — Bug 422: pytorch-lightning

- **Bug report:** [https://github.com/Lightning-AI/pytorch-lightning/issues/21635](https://github.com/Lightning-AI/pytorch-lightning/issues/21635)
- **Repository:** Lightning-AI/pytorch-lightning @ `612ab081e633861f6c7178b7e3e5eaf15b429b94`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Clone the referenced Lightning commit into codebase/ using setup_codebase.sh.
2. Run bash run_repro.sh.
3. Observe that the remote URI is normalized to s3:/... and FileNotFoundError is raised.

## Observed behavior

- input_uri=s3://my-bucket/checkpoints/epoch=5.ckpt
- pathlib_normalized=s3:/my-bucket/checkpoints/epoch=5.ckpt
- message=The provided path is not a valid DeepSpeed checkpoint: s3:/my-bucket/checkpoints/epoch=5.ckpt

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
