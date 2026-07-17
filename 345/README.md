# Bug 345 Reproduction

This folder reproduces the JAX build CLI failure reported in
`https://github.com/jax-ml/jax/issues/38969`.

The bug is triggered when a pip-installed `argparse` backport shadows the
standard library `argparse` module. Under that environment, JAX's
`codebase/build/build.py` fails at:

```python
subparsers = parser.add_subparsers(dest="command", required=True)
```

## Files

- `requirements.txt`: dependency pin needed to shadow stdlib `argparse`
- `setup_env.sh`: creates the isolated venv and installs dependencies
- `run_repro.sh`: runs the repro end-to-end
- `repro.py`: executes the failing JAX build CLI under the prepared env
- `reproduction.json`: machine-readable reproduction result
- `repro_stdout.log` / `repro_stderr.log`: captured command output

## Reproduction

Run:

```bash
bash run_repro.sh
```

Expected result:

- stdout shows that `argparse` is imported from the venv `site-packages`
- stderr ends with:

```text
TypeError: _SubParsersAction.__init__() got an unexpected keyword argument 'required'
```

