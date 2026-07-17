# Reproduction Trajectory — Bug 540: SDV

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2719](https://github.com/sdv-dev/SDV/issues/2719)
- **Repository:** sdv-dev/SDV @ `ae6e1c01a9b4d06bbc13868071a3ec36c5ed2d33`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a pandas DataFrame with one sequence key, two context columns, and two sequence columns.
2. Build Metadata with sequence_key='sequence' and instantiate PARSynthesizer with context_columns in reversed order.
3. Call synthesizer.fit(data) and observe the TypeError raised from deepecho/numpy.

## Observed behavior

- Running PARSynthesizer.fit() on the sample data with context_columns=['context2', 'context1'] crashes with TypeError: the resolved dtypes are not compatible with add.reduce. The traceback points into deepecho.models.par._idx_map via np.nanmean on the context values.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
