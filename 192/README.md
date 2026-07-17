# Bug 192

This folder is the reusable standardized benchmark input for the Real-IAD category mismatch.

Reused source inputs:
- `bug_report.txt`
- `codebase/`

Generated reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

What the repro does:
- Reads `codebase/src/anomalib/data/datasets/image/realiad.py`
- Extracts the hard-coded `CATEGORIES` tuple
- Compares it to the Real-IAD category list quoted in `bug_report.txt`
- Fails with a non-zero exit status when the lists differ

Run locally:
```bash
bash run_repro.sh
```

Issue reference:
- `https://github.com/open-edge-platform/anomalib/issues/2929`
