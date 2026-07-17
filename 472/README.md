# Bug 472

This folder contains the standardized reproduction bundle for
`https://github.com/pytorch/rl/issues/3463`.

What is included:
- `bug_report.txt`
- `codebase/` at `ab49b59dd37a4210f1d0102b89b7b00340217cf1`
- Reproduction artifacts

Reproduction summary:
- The bug is reproducible here on CUDA hardware.
- `TensorDictReplayBuffer` with `LazyTensorStorage(device="cuda:0", ndim=2)` and `SliceSampler(traj_key=("collector", "traj_ids"))` returns corrupted samples when a writer thread keeps calling `extend()` while the main thread samples.
- The failing run produced a mismatch at `step=130`:
  - `expected=1239`
  - `got_obs=1214.0`
  - `got_traj=1214`

Run it with:
```bash
bash setup_env.sh
bash run_repro.sh
```

Generated files:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`
