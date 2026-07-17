# Reproduction Trajectory — Bug 159: influxdb-client-python

- **Bug report:** [https://github.com/influxdata/influxdb-client-python/issues/603](https://github.com/influxdata/influxdb-client-python/issues/603)
- **Repository:** influxdata/influxdb-client-python @ `1ec64b7`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a Python 3.12 virtual environment and installed the runtime dependencies from `requirements.txt`.
2. Executed the repro from the standardized folder with `bash run_repro.sh`.
3. Observed `deprecation_warnings=1` and the `utcfromtimestamp` DeprecationWarning message in stdout.

## Observed behavior

- Running `bash run_repro.sh` under Python 3.12.3 imported `influxdb_client.client.write.point` and captured one DeprecationWarning from `datetime.datetime.utcfromtimestamp()`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
