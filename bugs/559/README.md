# Bug 559

This bundle reproduces the `Accelerator.reduce(..., reduction="mean")` bug from
`huggingface/accelerate#1112`.

What it does:
- loads the local `codebase/src` copy of Accelerate
- forces the reducer onto the distributed `MULTI_CPU` branch
- stubs `torch.distributed.all_reduce` to return the summed tensor
- shows that `reduction="mean"` returns the same value as `reduction="sum"`

Files:
- `repro.py` - minimal failing repro
- `requirements.txt` - runtime dependencies
- `setup_env.sh` - creates a clean venv and installs dependencies
- `run_repro.sh` - runs the repro in that venv

Run:
```bash
bash run_repro.sh
```

The script exits non-zero when the bug is present.
