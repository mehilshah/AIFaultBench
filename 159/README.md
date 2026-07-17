# Reproduction Bundle

This bundle reproduces the deprecation warning reported in `bug_report.txt`.

## What it checks

Importing `influxdb_client.client.write.point` on Python 3.12 emits a `DeprecationWarning` because `point.py` initializes `EPOCH` with `datetime.utcfromtimestamp(0)`.

## Run locally

```bash
bash run_repro.sh
```

## Expected output

The repro prints the imported module, the computed epoch value, and the captured deprecation warning message.
