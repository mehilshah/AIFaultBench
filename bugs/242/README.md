# Bug 242

This folder reproduces NumPyro issue https://github.com/pyro-ppl/numpyro/issues/1991.

Reproduction assets:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Observed behavior:
- `numpyro.infer.util.log_likelihood(...)` fails when the model uses `random_flax_module(...)`.
- The failure is a `ValueError` from `flax.core.scope.init` complaining about the init RNG argument.

Run:
- `bash run_repro.sh`
