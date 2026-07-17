# Bug 046 Reproduction Bundle

This folder reproduces the MMS forced-alignment shape failure from fairseq issue 5242.

The failure path is in `codebase/examples/mms/data_prep/align_and_segment.py`, which builds a 2-D emission tensor and passes it to `torchaudio.functional.forced_align`. Current torchaudio expects `log_probs` to be 3-D `(batch_size, input_length, num_classes)`, so the call raises:

`RuntimeError: log_probs must be 3-D (batch_size, input length, num classes)`

Contents:
- `repro.py`: minimal reproducer
- `requirements.txt`: pinned Python deps for the repro
- `setup_env.sh`: create a local virtualenv and install deps
- `run_repro.sh`: execute the repro and capture logs
- `manifest.json`: standardized metadata
- `reproduction.json`: final result written after running the repro
- `repro_stdout.log` / `repro_stderr.log`: captured execution output

Reproduction command:

```bash
bash run_repro.sh
```
