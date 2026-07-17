# Reproduction Trajectory — Bug 180: lightning

- **Bug report:** [https://github.com/Lightning-AI/pytorch-lightning/issues/20628](https://github.com/Lightning-AI/pytorch-lightning/issues/20628)
- **Repository:** Lightning-AI/pytorch-lightning @ `1f5add3`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a virtualenv and install the runtime dependencies with `bash setup_env.sh`.
2. Run the repro with `bash run_repro.sh` so `PYTHONPATH` points at `codebase/src` and the legacy `pytorch_lightning` namespace is available from the local source tree.
3. Observe the `ValueError: Expected a parent` traceback during `Trainer(callbacks=[MyCallback])` initialization.

## Observed behavior

- Running `bash run_repro.sh` printed `isinstance(MyCallback, NewCallback)=False` and then failed in `lightning/pytorch/trainer/connectors/callback_connector.py::_validate_callbacks_list()` with `ValueError: Expected a parent` from `lightning/pytorch/utilities/model_helpers.py::is_overridden()`. The mixed-import check misses the callback class because it inspects `type(instance)` instead of the class itself.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
