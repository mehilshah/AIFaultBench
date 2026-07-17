# Reproduction Trajectory — Bug 490: detectron2

- **Bug report:** [https://github.com/facebookresearch/detectron2/issues/56](https://github.com/facebookresearch/detectron2/issues/56)
- **Repository:** facebookresearch/detectron2 @ `0c28c3d9f1141ad5d6ac4ba6efe306d38048981e`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Build the repro image with `bash run_repro.sh`.
2. Run the resulting container without `--gpus` so it has no NVIDIA runtime access.
3. Observe the `RuntimeError` when the script moves a tensor to CUDA.

## Observed behavior

- Docker build succeeded and the container run failed exactly at the CUDA handoff: `torch_version=2.3.1`, `cuda_is_available=False`, then `torch.zeros(1).cuda()` raised `RuntimeError: Found no NVIDIA driver on your system. Please check that you have an NVIDIA GPU and installed a driver from http://www.nvidia.com/Download/index.aspx`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
