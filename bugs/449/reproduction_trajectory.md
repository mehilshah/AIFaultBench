# Reproduction Trajectory — Bug 449: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/46909](https://github.com/huggingface/transformers/issues/46909)
- **Repository:** huggingface/transformers @ `7b89511f58828f90e86ee118a4fd693bbebe7ba3`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Run ./run_repro.sh in the standardized bug folder.
2. The script executes the documented DIA example in three stages and captures the first failing line in each stage.

## Observed behavior

- phase_1_missing_model: NameError: name 'model' is not defined
- phase_2_missing_torch_device: NameError: name 'torch_device' is not defined
- phase_3_invalid_device_map_kwarg: TypeError: to() got an unexpected keyword argument 'device_map'

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
