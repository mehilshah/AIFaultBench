# Reproduction Trajectory — Bug 220: tensorflow-datasets

- **Bug report:** [https://github.com/tensorflow/datasets/issues/5397](https://github.com/tensorflow/datasets/issues/5397)
- **Repository:** tensorflow/datasets @ `d5401a0`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a local virtual environment and installed the TFDS runtime dependencies plus the editable codebase snapshot.
2. Loaded the checked-in plant_leaves checksum metadata from codebase/tensorflow_datasets/datasets/plant_leaves/checksums.tsv.
3. Probed the reported upstream dataset URL and observed HTTP 403.
4. Validated a tiny local archive against the reported checksum and observed tensorflow_datasets.core.download.download_manager.NonMatchingChecksumError.

## Observed behavior

- The local TFDS checksum validator raises NonMatchingChecksumError when the reported plant_leaves checksum metadata is compared against a tiny local archive, but the live upstream URL from the report now returns HTTP 403 in this environment.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```

## Why it does not reproduce on the reference machine

The exact upstream dataset artifact is no longer downloadable here, so the original remote checksum mismatch from the report cannot be reproduced directly.
