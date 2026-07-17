# Bug 120

This folder contains a self-contained reproduction bundle for stable-baselines3 issue 1634.

Inputs reused from the benchmark:
- `bug_report.txt`
- `codebase/`

Generated artifacts in this folder:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Repro summary:
- The logger writes a `torch.Tensor` histogram to TensorBoard.
- The same logger call with `np.ndarray` does not produce a histogram event.
