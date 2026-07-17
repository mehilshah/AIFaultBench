# Bug 492

Reproduction bundle for `numpyro` issue `#2040`.

Observed failure:

- `numpyro==0.10.1`
- `jax==0.4.38`
- `jaxlib==0.4.38`
- `import numpyro` fails during import with `ModuleNotFoundError: No module named 'jax.linear_util'`

Files in this folder:

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

Reproduction command:

```bash
bash run_repro.sh
```
