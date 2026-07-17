# Reproduction Trajectory — Bug 294: pyro

- **Bug report:** [https://github.com/pyro-ppl/pyro/issues/3365](https://github.com/pyro-ppl/pyro/issues/3365)
- **Repository:** pyro-ppl/pyro @ `ca36025a3502c0160395b53145d2e95b56eaf15f`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Imported the local pyro code from codebase/.
2. Rendered the PyroModule model with module_local_params=True and False.
3. Observed KeyError: 'constraint' only when module_local_params=True.

## Observed behavior

- With module_local_params=True, pyro.render_model(Model()) raised KeyError: 'constraint'. With module_local_params=False, the same model rendered successfully.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
