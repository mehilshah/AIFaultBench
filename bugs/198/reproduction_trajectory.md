# Reproduction Trajectory — Bug 198: modelscan

- **Bug report:** [https://github.com/protectai/modelscan/issues/93](https://github.com/protectai/modelscan/issues/93)
- **Repository:** protectai/modelscan @ `a647a2b`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a minimal HDF5 file without a model_config attribute.
2. Run modelscan CLI against the file with PYTHONPATH pointing at codebase/.
3. Observe the TypeError surfaced as 'Exception: the JSON object must be str, bytes or bytearray, not dict'.

## Observed behavior

- modelscan.cli exited with code 2 and printed 'Exception: the JSON object must be str, bytes or bytearray, not dict' while scanning a valid HDF5 file with no model_config attribute.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
