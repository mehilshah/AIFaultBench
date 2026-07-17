# Bug 635

This folder contains the standardized reproduction bundle for the profiling
bound-method bug reported in diffusers issue 13462.

Files:
- `bug_report.txt`
- `codebase/`
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction approach:
- use the real `annotate_pipeline()` implementation from
  `codebase/examples/profiling/profiling_utils.py`
- wrap a dummy scheduler method exactly as the profiling helper does
- deep-copy the scheduler to simulate the LTX2 pipeline's duplicated scheduler
- show that the copied scheduler still calls the original instance

Environment note:
- this folder ships a small local `torch` compatibility shim so the repro does
  not depend on the host's CUDA PyTorch installation

Reproduction command:
- `bash run_repro.sh`
