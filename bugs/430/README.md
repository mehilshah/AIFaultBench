# Bug 430

This folder is the reusable standardized benchmark input for this bug.

Reused from the raw benchmark folder:
- `bug_report.txt`
- `codebase/` when available

Reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Source summary:
- issue URL: `https://github.com/pyro-ppl/pyro/issues/3203`
- commit hash: `dd4e0f81b4ddceb82ebd663b20333e175ce27c2a`
- inferred library: `pyro`
- inferred library version: `unknown`
- runtime torch version: `2.13.0+cpu`
- bug report source: `bug_report.txt`
- codebase source: `pyro-ppl/pyro@dd4e0f81b4ddceb82ebd663b20333e175ce27c2a`
- repro notes: `repro.py` removes `torch.distributions.constraints._CorrCholesky` at runtime to exercise the target commit's uncaught AttributeError path.
