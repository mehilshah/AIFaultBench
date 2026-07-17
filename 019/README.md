# Bug 019 Repro

Issue: [`tensorflow/models#11018`](https://github.com/tensorflow/models/issues/11018)

The reproduced failure here is an import-time ABI mismatch in `tensorflow_text`.
In this standardized folder, the local `codebase/` import path still reaches the
TF-Text load path from `tensorflow_models`, and a direct `tensorflow_text`
import in the same environment raises the same undefined-symbol error.

## Reproduction

```bash
bash run_repro.sh
```

## Files

- `bug_report.txt`: source issue report
- `codebase/`: local TensorFlow Model Garden snapshot
- `repro.py`: import sequence that exercises the bug path
- `requirements.txt`: pinned repro dependencies
- `setup_env.sh`: creates the isolated Python environment
- `run_repro.sh`: runs setup and captures logs
- `manifest.json`: metadata for the standardized bundle
- `repro_stdout.log`, `repro_stderr.log`: captured command output

