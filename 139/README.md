# Bug 139

Reproduction bundle for `timm` issue 2282.

What this bundle contains:
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

Result:
- Reproducible in this workspace.
- The first row of the MLP output differs between batch size 1 and batch size 2, even with identical inputs.
- Observed on `torch 2.7.0+cu128` with an NVIDIA RTX PRO 6000 Blackwell GPU.
- The report’s exact `torch 2.4.1+cu118` wheel was not usable on this GPU because it lacks `sm_120` support.

Run:
```bash
bash run_repro.sh
```
