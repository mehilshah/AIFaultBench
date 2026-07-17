# Bug 356

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

Reproduction summary:
- The checked-out `codebase/` already exports `InverseWishart` from `numpyro.distributions`.
- Loading `numpyro.distributions` directly from source shows `hasattr(dist, "InverseWishart") == True`.
- A full `import numpyro.distributions` is blocked here by an unrelated JAX API mismatch in `numpyro.__init__` / `numpyro.ops.provenance`.

Source summary:
- issue URL: `https://github.com/pyro-ppl/numpyro/issues/2130`
- commit hash: `c5fce4e3df4699e3913e0538fe3efffcabbc026b`
- inferred library: `numpyro`
- inferred library version: `0.19.0`
- bug report source: `bug_report.txt`
- codebase source: `pyro-ppl/numpyro@c5fce4e3df4699e3913e0538fe3efffcabbc026b`
