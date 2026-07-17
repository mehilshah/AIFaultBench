# Bug 342

Reproduction bundle for Pyro issue `https://github.com/pyro-ppl/pyro/issues/3301`.

Observed behavior in this checkout:
- `ZeroInflatedPoisson(rate=..., gate_logits=logit)` and `ZeroInflatedPoisson(rate=..., gate=p)` both sample zeros at about the requested rate
- The issue report does not reproduce here

Run it:
1. `bash setup_env.sh`
2. `bash run_repro.sh`

Bundle contents:
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
