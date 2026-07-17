# Reproduction Trajectory — Bug 592: SDV

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2708](https://github.com/sdv-dev/SDV/issues/2708)
- **Repository:** sdv-dev/SDV @ `049106473fd32f00d2b551ef61864801792acc2c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a minimal single-table fixture with a primary key column named id.
2. Call DayZSynthesizer.create_parameters on the fixture to generate a valid parameter dict.
3. Mutate the generated primary-key entry so missing_values_proportion becomes 0.5.
4. Call DayZSynthesizer.validate_parameters and observe that it does not raise SynthesizerProcessingError.
5. Fail the repro with an AssertionError to record the incorrect acceptance.

## Observed behavior

- repro_stdout.log shows CREATED_PARAMETERS with the primary key id assigned missing_values_proportion 0.0, then VALIDATION_ACCEPTED_NONZERO_PRIMARY_KEY_MISSING_VALUES_PROPORTION after mutating that key to 0.5. repro_stderr.log ends with AssertionError: validate_parameters accepted a nonzero 'missing_values_proportion' for the primary key.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
