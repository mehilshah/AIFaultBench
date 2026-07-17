# Reproduction Trajectory — Bug 160: influxdb-client-python

- **Bug report:** [https://github.com/influxdata/influxdb-client-python/issues/623](https://github.com/influxdata/influxdb-client-python/issues/623)
- **Repository:** influxdata/influxdb-client-python @ `eb5afd1`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a self-contained virtual environment and installed the local `codebase/` in editable mode with its runtime dependencies.
2. Ran `repro.py` with two structurally identical `Point` objects.
3. Observed `line_protocol_equal: True` and `point_equality: False` in `repro_stdout.log`.

## Observed behavior

- Two Point instances with identical measurement, tags, fields, and timestamp produced identical line protocol, but `point_a == point_b` evaluated to `False` in the local snapshot.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
