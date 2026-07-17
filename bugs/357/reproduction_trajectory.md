# Reproduction Trajectory — Bug 357: pyro

- **Bug report:** [https://github.com/pyro-ppl/pyro/issues/3276](https://github.com/pyro-ppl/pyro/issues/3276)
- **Repository:** pyro-ppl/pyro @ `c00bcc3fb701327b07e94de88754da49b7f29ebe`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a clean virtualenv and install mypy==1.5.1 plus numpy==1.26.4.
2. Run mypy against repro.py using codebase/setup.cfg, which keeps python_version at 3.7.
3. Observe that mypy fails while parsing NumPy's typing file.

## Observed behavior

- Running ./.venv/bin/mypy --cache-dir .mypy_cache --install-types --non-interactive --config-file codebase/setup.cfg repro.py exits with status 2.
- stderr reports: .venv/lib/python3.12/site-packages/numpy/_typing/_nested_sequence.py:60: error: Positional-only parameters are only supported in Python 3.8 and greater  [syntax]

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./.venv/bin/mypy --cache-dir .mypy_cache --install-types --non-interactive --config-file codebase/setup.cfg repro.py
```
