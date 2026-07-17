# Reproduction Trajectory — Bug 213: sdv

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2366](https://github.com/sdv-dev/SDV/issues/2366)
- **Repository:** sdv-dev/SDV @ `c1c5a19`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a local venv with `bash setup_env.sh`.
2. Run `bash run_repro.sh` from the bug folder.
3. Observe that `sample_from_conditions()` on an unfitted `GaussianCopulaSynthesizer` raises `sdv.data_processing.errors.NotFittedError` instead of a proactive fitting-first `SamplingError`.

## Observed behavior

- Running `GaussianCopulaSynthesizer(metadata).sample_from_conditions(...)` on the unfitted demo model raises `sdv.data_processing.errors.NotFittedError` with the wrapped message `Error: Sampling terminated. No results were saved due to unspecified "output_file_path".` The traceback shows the original `NotFittedError` comes from `DataProcessor.transform()` and is then re-raised by `handle_sampling_error()`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh > repro_stdout.log 2> repro_stderr.log
```
