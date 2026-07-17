# Bug 282

This folder is the reusable standardized benchmark input for JAX issue 39145.

Reused from the raw benchmark folder:
- `bug_report.txt`
- `codebase/`

Reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction summary:
- issue URL: `https://github.com/jax-ml/jax/issues/39145`
- bug-era release reproduced here: `jax 0.10.2` with `jax-cuda12-plugin 0.10.2`
- current local source tree checked separately: `jax 0.11.0.dev20260717`
- outcome: reproducible on the pinned 0.10.2 CUDA release
- observed behavior: GPU memory stayed elevated after `del + gc` and grew to about `6.6 GiB` after the scratch loop instead of returning near the baseline

Run the repro bundle:

```bash
bash setup_env.sh
bash run_repro.sh
```

The repro is intentionally scaled down from the issue report because this machine already has other GPU workloads running.
