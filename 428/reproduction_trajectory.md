# Reproduction Trajectory — Bug 428: detectron2

- **Bug report:** [https://github.com/facebookresearch/detectron2/issues/856](https://github.com/facebookresearch/detectron2/issues/856)
- **Repository:** facebookresearch/detectron2 @ `41d475b75a230221e21d9cac5d69655e3415e3a4`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Load codebase/detectron2/structures/masks.py with minimal runtime stubs for unrelated dependencies.
2. Instantiate PolygonMasks with a simple polygon list.
3. Access PolygonMasks.device.

## Observed behavior

- Running the repro script constructs a PolygonMasks instance from polygon coordinates and then crashes when accessing PolygonMasks.device with AttributeError: 'PolygonMasks' object has no attribute 'tensor'.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
