# Bug 223

Reproduction bundle for the Triton launcher bug described in `bug_report.txt`.

What this bundle does:
- Uses a file-backed `@triton.jit` kernel so `inspect.getsourcelines()` succeeds.
- Replaces Triton driver/compile hooks with tiny fakes so the repro reaches the real
  `JITFunction.run()` grid canonicalization code path without requiring CUDA.
- Passes a grid callable that returns an `int`, which triggers the `len(grid)` failure.

Files:
- `repro.py` - minimal reproducer
- `requirements.txt` - Python dependency pinning
- `setup_env.sh` - environment bootstrap
- `run_repro.sh` - executes the reproducer
- `manifest.json` - standardized metadata

Repro status in this folder:
- reproducible: yes
- observed exception: `TypeError: object of type 'int' has no len()`
- trigger location: `triton/runtime/jit.py` in `JITFunction.run()`

Issue reference:
- `https://github.com/triton-inference-server/server/issues/7967`
