# Bug 291

This folder contains a self-contained repro for detectron2 issue 3591.

Observed failure:
- `BitMasks.__getitem__` handles `masks[4]` with `self.tensor[item].view(1, -1)`.
- That flattens the mask to shape `[1, 65536]`, which fails the `BitMasks` constructor assertion that the tensor must be 3D.

Run:
```bash
bash run_repro.sh
```

Artifacts:
- `repro.py`: minimal reproducer
- `requirements.txt`: runtime dependencies
- `setup_env.sh`: dependency install helper
- `run_repro.sh`: wrapper that captures stdout/stderr
- `reproduction.json`: schema-constrained result summary
- `repro_stdout.log` and `repro_stderr.log`: captured output from the repro run

Source:
- issue URL: `https://github.com/facebookresearch/detectron2/issues/3591`
- code path: [`codebase/detectron2/structures/masks.py`](codebase/detectron2/structures/masks.py)
