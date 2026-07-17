# Bug 070 Reproduction Bundle

This folder contains a standalone reproduction for the Domino/DeepSpeed bug reported in:

- `https://github.com/deepspeedai/DeepSpeedExamples/issues/948`

Observed failure:

- `AttributeError: 'NoneType' object has no attribute 'all_reduce'`

Root cause inferred from the codebase:

- `codebase/training/DeepSpeed-Domino/domino/initialize.py` initializes `torch.distributed`
  but does not initialize the DeepSpeed communication backend.
- `codebase/training/DeepSpeed-Domino/domino/training.py` later calls `deepspeed.comm.all_reduce`,
  which expects DeepSpeed's `cdb` backend object to be set.

Files in this bundle:

- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Run:

```bash
bash run_repro.sh
```

