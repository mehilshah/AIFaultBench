# Reproduction Trajectory — Bug 216: freezegun

- **Bug report:** [https://github.com/spulec/freezegun/issues/344](https://github.com/spulec/freezegun/issues/344)
- **Repository:** spulec/freezegun @ `c8806fa`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Run `bash run_repro.sh` from the standardized bug folder.
2. The script creates a local `.venv`, installs `six` and `python-dateutil`, and executes `repro.py`.
3. Observe that the round-trip timestamp equality fails under `tz_offset=-1` and the script exits with AssertionError.

## Observed behavior

- On freezegun 0.3.15, the baseline round-trip passes, but under freeze_time(datetime.datetime.fromtimestamp(100000), tz_offset=-1) the repro prints baseline_equal=True, then frozen_now=1970-01-01 22:46:40, timestamp=85600.0, round_trip_timestamp=96400.0, equal=False. The script then raises AssertionError: Expected t == datetime.fromtimestamp(t).timestamp() under tz_offset=-1, but got t=85600.0 and t2=96400.0.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
