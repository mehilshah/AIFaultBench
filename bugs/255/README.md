# Bug 255 Reproduction Bundle

This bundle reproduces the timing-helper bug described in `bug_report.txt`.

## What it checks

- `codebase/intermediate_source/torch_compile_tutorial.py` contains the helper that divides CUDA event milliseconds by `1024`.
- `codebase/intermediate_source/torch_compile_full_example.py` shows the corrected `/ 1000` version.
- `repro.py` demonstrates the numerical mismatch using a 1024 ms example.

## Run

```bash
bash run_repro.sh
```

The run writes stdout to `repro_stdout.log` and stderr to `repro_stderr.log`.
