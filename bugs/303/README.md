# Bug 303

Reproduction bundle for DeepSpeed issue 7971, focused on the `fp_quantizer`
CUDA implementation warnings reported in `bug_report.txt`.

## Contents

- `bug_report.txt`
- `codebase/`
- `fp_quantizer_warning_repro.cu`
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

## Repro command

```bash
bash run_repro.sh
```

The repro is compile-only. It uses `nvcc` to compile a minimal CUDA translation
unit that mirrors the warning-triggering expressions from
`codebase/csrc/fp_quantizer/fp_quantize_impl.cu`.

