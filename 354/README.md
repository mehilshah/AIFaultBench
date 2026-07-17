# Detectron2 TTA negative-stride repro

This bundle reproduces the bug reported in detectron2 issue 2236.

The failure comes from `GeneralizedRCNNWithTTA.__call__` reading an image from `file_name`, passing it through `read_image(..., format="BGR")`, and then converting the resulting NumPy array with `torch.from_numpy(...)`. In the BGR branch, the channel reversal creates a view with a negative stride, which PyTorch rejects.

The repro script mirrors the exact BGR conversion used by `detectron2.data.detection_utils.convert_PIL_to_numpy(...)`.

## How to run

```bash
bash run_repro.sh
```

Expected result:

```text
ValueError: At least one stride in the given numpy array is negative
```

The command writes stdout to `repro_stdout.log` and stderr to `repro_stderr.log`.
